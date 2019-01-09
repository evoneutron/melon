import os
import multiprocessing

from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from pathlib import Path
from tqdm import tqdm

from melon.imgmelon_denominations import Denominations as denom
from melon.melon import Melon

try:
    from PIL import Image as pil_image
except ImportError:
    pil_image = None


class ImageMelon(Melon):
    __default_data_format = "channels_first"
    __default_channels = 3
    __default_height = 255
    __default_width = 255
    __default_normalize = False
    __default_preserve_aspect_ratio = False
    __default_num_threads = 4
    __unsupported_file_formats = [".svg"]

    def __init__(self, options=None):
        self.__target_height = options.get(denom.height) if options and options.get(denom.height) else self.__default_height
        self.__target_width = options.get(denom.width) if options and options.get(denom.width) else self.__default_width
        self.__target_channels = options.get(denom.channels) if options and options.get(denom.channels) else self.__default_channels
        self.__target_format = options.get(denom.data_format) if options and options.get(denom.data_format) else self.__default_data_format
        self.__normalize = options.get(denom.normalize) if options and options.get(denom.normalize) else self.__default_normalize
        self.__preserve_aspect_ratio = options.get(denom.preserve_aspect_ratio) if options and options.get(
            denom.preserve_aspect_ratio) else self.__default_preserve_aspect_ratio

        try:
            self.__num_threads = options.get(denom.num_threads) if options and options.get(
                denom.num_threads) else multiprocessing.cpu_count()
            print("Number of workers set to {}".format(self.__num_threads))
        except NotImplementedError:
            self.__num_threads = self.__default_num_threads

    def interpret(self, source_dir):
        """
        Logic to interpret the images into the output format of "mxCxHxW or mxHxWxC"
        :param source_dir: source_sample directory of the files
        :return: tuple of 4-D array of "mxCxHxW or mxHxWxC" and labels
        """
        dir = Path(source_dir)
        labels = self.__read_labels(dir)
        files = self._list_and_validate(labels, dir)
        m = len(files)

        y = np.empty(m, dtype=np.int32)
        if self.__target_format == "channels_first":
            x = np.ndarray(shape=(m, self.__target_channels, self.__target_height, self.__target_width), dtype=np.float32)
        elif self.__target_format == "channels_last":
            x = np.ndarray(shape=(m, self.__target_height, self.__target_width, self.__target_channels), dtype=np.float32)
        else:
            raise ValueError("Unknown data format %s" % self.__target_format)

        with tqdm(total=m, unit="file", desc="Total") as pbar:
            with ThreadPoolExecutor(max_workers=self.__num_threads) as executor:
                batch_size = m // self.__num_threads
                remainder = m % self.__num_threads
                end = m - remainder

                futures = []

                for i in range(0, end, batch_size):
                    batch_start = i
                    batch_end = i + batch_size + (0 if (i + batch_size < end) else remainder)
                    future = executor.submit(self.__worker, files[batch_start:batch_end], batch_start, x, y, labels, pbar)
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        future_result = future.result()
                    except Exception:
                        print("Failed to retrieve future result")
        return x, y

    def _validate_file(self, labels, file):
        if file.name.startswith("labels"):
            return False
        if file.suffix in self.__unsupported_file_formats:
            print("Unsupported file format %s" % file.suffix)  # log.err and track
            return False

        label = labels.get(file.stem) or labels.get(file.name)
        if not label:
            print("Unable to map label to an image file %s" % file)  # log.err and track
            return False
        return True

    def __read_labels(self, dir):
        """
        Reads labels file and returns mapping of file to label
        :param dir: source directory
        :return: dictionary of file to label mapping
        """
        labels_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.startswith("labels")]
        if not labels_files:
            raise ValueError("Unable to locate labels file. Make sure labels file is in the source directory.")

        result = {}
        file = Path(dir / labels_files[0])
        read_files = False
        with open(file) as infile:
            for line in infile:
                line = line.strip()
                if not line: continue
                if line == "#map":
                    read_files = True
                    continue
                if read_files:
                    parts = line.split(":")
                    if len(parts) != 2:
                        print("Malformed line")  # log.err
                    result[parts[0].strip()] = int(parts[1].strip())
        return result

    def __img_to_arr(self, img_file, dtype='float32'):
        img = pil_image.open(img_file)
        with img:
            hsize = self.__target_height
            if self.__preserve_aspect_ratio:
                wpercent = (self.__target_width / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((self.__target_width, hsize), pil_image.BICUBIC)
            arr = np.asarray(img, dtype=dtype)
            if len(arr.shape) == 3:
                # RGB
                if self.__target_format == 'channels_first': arr = arr.transpose(2, 0, 1)
            elif len(arr.shape) == 2:
                if self.__target_format == 'channels_first':
                    arr = arr.reshape((1, arr.shape[0], arr.shape[1]))
                else:
                    arr = arr.reshape((arr.shape[0], arr.shape[1], 1))
            else:
                raise ValueError('Unsupported image shape: %s' % (arr.shape,))

            if self.__normalize:
                arr /= self.__target_width

        return arr

    def __worker(self, batch, index, x, y, labels, pbar):
        start = str(index)
        end = str(index + len(batch) - 1)

        for file in batch:
            label = labels.get(file.stem) or labels.get(file.name)
            x[index] = self.__img_to_arr(file)
            y[index] = label
            index += 1
            pbar.update(1)

        return "Processed batch [{},{}]".format(start, end)
