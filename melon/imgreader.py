import logging
import multiprocessing
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from tqdm import tqdm

from melon.imgreader_denominations import Denominations as denom
from melon.reader import Reader

try:
    from PIL import Image as pil_image

    logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
except ImportError:
    pil_image = None


class ImageReader(Reader):
    __default_data_format = "channels_first"
    __default_channels = 3
    __default_height = 255
    __default_width = 255
    __default_normalize = False
    __default_preserve_aspect_ratio = False
    __default_num_threads = 4
    __unsupported_file_formats = [".svg"]

    def __init__(self, source_dir, options=None):
        """
        :param source_dir: source directory of the image files
        :param options: reader options
        """
        self.__source_dir = source_dir
        self.__target_height = options.get(denom.height) if options and options.get(denom.height) else self.__default_height
        self.__target_width = options.get(denom.width) if options and options.get(denom.width) else self.__default_width
        self.__target_format = options.get(denom.data_format) if options and options.get(denom.data_format) else self.__default_data_format
        self.__normalize = options.get(denom.normalize) if options and options.get(denom.normalize) else self.__default_normalize
        self.__preserve_aspect_ratio = options.get(denom.preserve_aspect_ratio) if options and options.get(
            denom.preserve_aspect_ratio) else self.__default_preserve_aspect_ratio
        self.__offset = 0
        self.__log = logging.getLogger(__name__)

        try:
            self.__num_threads = options.get(denom.num_threads) if options and options.get(
                denom.num_threads) else multiprocessing.cpu_count()
            self.__log.info("Number of workers set to %s", self.__num_threads)
        except NotImplementedError:
            self.__num_threads = self.__default_num_threads

        self.__labels, self.__files = self.__read_meta()
        if options and options.get(denom.batch_size):
            self.__batch_size = min(options.get(denom.batch_size), len(self.__files))
        else:
            self.__batch_size = len(self.__files)

    def read(self):
        """
        Logic to read the images into the output format of "mxCxHxW or mxHxWxC"
        :param
        :return: tuple of 4-D array of "mxCxHxW or mxHxWxC" and labels
        """
        try:
            files = self.__files[self.__offset:self.__offset + self.__batch_size]
            m = len(files)

            y = np.empty(m, dtype=np.int32)
            if self.__target_format == "channels_first":
                x = np.ndarray(shape=(m, self.__default_channels, self.__target_height, self.__target_width),
                               dtype=np.float32)
            elif self.__target_format == "channels_last":
                x = np.ndarray(shape=(m, self.__target_height, self.__target_width, self.__default_channels),
                               dtype=np.float32)
            else:
                raise ValueError("Unknown data format %s" % self.__target_format)

            with tqdm(total=m, unit="file", desc="Total", leave=False) as pbar:
                with ThreadPoolExecutor(max_workers=self.__num_threads) as executor:
                    thread_batch_size = max(1, m // self.__num_threads)
                    remainder = m % self.__num_threads

                    futures = []
                    for i in range(0, m, thread_batch_size):
                        batch_start = i
                        is_final_batch = (i == m - remainder - thread_batch_size)
                        batch_end = i + thread_batch_size + (remainder if is_final_batch else 0)

                        future = executor.submit(self.__worker, files[batch_start:batch_end], batch_start, x, y, pbar)
                        futures.append(future)
                        if is_final_batch:
                            break

                    for future in as_completed(futures):
                        try:
                            future_result = future.result()
                        except Exception  as e:
                            self.__log.error("Failed to get future {}".format(str(e)))
            return x, y

        finally:
            self.__offset += self.__batch_size

    def has_next(self):
        return self.__offset < len(self.__files)

    def _validate_file(self, file):
        if file.suffix in self.__unsupported_file_formats:
            self.__log.warning("Unsupported file format %s", file.suffix)
            return False
        if file.name.startswith("labels") or file.name.startswith("."):
            return False
        return True

    def __read_meta(self):
        dir = Path(self.__source_dir)
        try:
            labels = self.__read_labels(dir)
        except Exception as e:
            raise ValueError("Failed to read labels. {}".format(str(e)))

        try:
            files = self._list_and_validate(dir)
        except Exception as e:
            raise ValueError("Failed to read image files. {}".format(str(e)))
        return labels, files

    def __read_labels(self, dir):
        """
        Reads labels file and returns mapping of file to label
        :pararm dir: source directory
        :return: dictionary of file to label mapping
        """
        result = {}
        labels_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.startswith("labels")]
        if not labels_files:
            self.__log.info("No labels file provided. Label vector will not be loaded.")
            return result

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
                        self.__log.warning("Malformed line in labels file %s", line)
                        continue
                    label = parts[1].strip()
                    result[parts[0].strip()] = int(label) if label else None
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
                if self.__target_format == 'channels_first':
                    arr = arr.transpose(2, 0, 1)
            elif len(arr.shape) == 2:
                # Greyscale
                if self.__target_format == 'channels_first':
                    arr = arr.reshape((1, arr.shape[0], arr.shape[1]))
                else:
                    arr = arr.reshape((arr.shape[0], arr.shape[1], 1))
            else:
                raise ValueError('Unsupported image shape: %s' % (arr.shape,))

            if self.__normalize:
                arr /= self.__target_width

        return arr

    def __worker(self, batch, index, x, y, pbar):
        start = str(index)
        end = str(index + len(batch) - 1)

        for file in batch:
            label = self.__labels.get(file.name) if file.name in self.__labels else -1
            x[index] = self.__img_to_arr(file)
            y[index] = label
            index += 1
            pbar.update(1)

        return "Processed batch [{},{}]".format(start, end)
