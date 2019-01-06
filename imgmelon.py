import os
import numpy as np
from imgmelon_denominations import Denominations as denom

try:
    from PIL import Image as pil_image
except ImportError:
    pil_image = None
    ImageEnhance = None


class Interpreter:
    default_data_format = "channels_first"
    default_channels = 3
    default_height = 255
    default_width = 255
    default_normalize = False
    default_preserve_aspect_ratio = False

    def __init__(self, options=None):
        self.target_height = options.get(denom.height) if options and options.get(denom.height) else self.default_height
        self.target_width = options.get(denom.width) if options and options.get(denom.width) else self.default_width
        self.target_channels = options.get(denom.channels) if options and options.get(denom.channels) else self.default_channels
        self.target_format = options.get(denom.data_format) if options and options.get(denom.data_format) else self.default_data_format
        self.normalize = options.get(denom.normalize) if options and options.get(denom.normalize) else self.default_normalize
        self.preserve_aspect_ratio = options.get(denom.preserve_aspect_ratio) if options and options.get(
            denom.preserve_aspect_ratio) else self.default_preserve_aspect_ratio

    def interpret(self, source_dir):
        """
        Logic to interpret the images into the output format of "mxCxHxW or mxHxWxC"
        :param source_dir: source_sample directory of the files
        :return: 4-D array of "mxCxHxW or mxHxWxC"
        """
        only_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        if self.target_format == "channels_first":
            result = np.ndarray(shape=(len(only_files), self.target_channels, self.target_height, self.target_width), dtype=np.float32)
        elif self.target_format == "channels_last":
            result = np.ndarray(shape=(len(only_files), self.target_height, self.target_width, self.target_channels), dtype=np.float32)
        else:
            raise ValueError("Unknown data format %s" % self.target_format)

        for i, f in enumerate(only_files):
            result[i] = self.img_to_array(source_dir + "/" + f)

        return result

    def img_to_array(self, img_file, dtype='float32'):
        img = pil_image.open(img_file)
        with img:
            hsize = self.target_height
            if self.preserve_aspect_ratio:
                wpercent = (self.target_width / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((self.target_width, hsize), pil_image.BICUBIC)

            arr = np.asarray(img, dtype=dtype)
            if len(arr.shape) == 3:
                # RGB
                if self.target_format == 'channels_first': arr = arr.transpose(2, 0, 1)
            elif len(arr.shape) == 2:
                if self.target_format == 'channels_first':
                    arr = arr.reshape((1, arr.shape[0], arr.shape[1]))
                else:
                    arr = arr.reshape((arr.shape[0], arr.shape[1], 1))
            else:
                raise ValueError('Unsupported image shape: %s' % (arr.shape,))

            if self.normalize:
                arr /= self.target_width

        return arr
