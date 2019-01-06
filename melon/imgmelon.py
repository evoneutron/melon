import os
import numpy as np
from melon.imgmelon_denominations import Denominations as denom

try:
    from PIL import Image as pil_image
except ImportError:
    pil_image = None
    ImageEnhance = None


class ImageMelon:
    __default_data_format = "channels_first"
    __default_channels = 3
    __default_height = 255
    __default_width = 255
    __default_normalize = False
    __default_preserve_aspect_ratio = False

    def __init__(self, options=None):
        self.__target_height = options.get(denom.height) if options and options.get(denom.height) else self.__default_height
        self.__target_width = options.get(denom.width) if options and options.get(denom.width) else self.__default_width
        self.__target_channels = options.get(denom.channels) if options and options.get(denom.channels) else self.__default_channels
        self.__target_format = options.get(denom.data_format) if options and options.get(denom.data_format) else self.__default_data_format
        self.__normalize = options.get(denom.normalize) if options and options.get(denom.normalize) else self.__default_normalize
        self.__preserve_aspect_ratio = options.get(denom.preserve_aspect_ratio) if options and options.get(
            denom.preserve_aspect_ratio) else self.__default_preserve_aspect_ratio

    def interpret(self, source_dir):
        """
        Logic to interpret the images into the output format of "mxCxHxW or mxHxWxC"
        :param source_dir: source_sample directory of the files
        :return: 4-D array of "mxCxHxW or mxHxWxC"
        """
        only_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        if self.__target_format == "channels_first":
            result = np.ndarray(shape=(len(only_files), self.__target_channels, self.__target_height, self.__target_width),
                                dtype=np.float32)
        elif self.__target_format == "channels_last":
            result = np.ndarray(shape=(len(only_files), self.__target_height, self.__target_width, self.__target_channels),
                                dtype=np.float32)
        else:
            raise ValueError("Unknown data format %s" % self.__target_format)

        for i, f in enumerate(only_files):
            result[i] = self.__img_to_array(source_dir + "/" + f)

        return result

    def __img_to_array(self, img_file, dtype='float32'):
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
