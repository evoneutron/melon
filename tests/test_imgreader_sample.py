import pathlib
from unittest import TestCase, mock, main

import numpy

from melon import ImageReader


class ImageReaderTestCase(TestCase):
    _tests_dir = "tests/resources/images/sample"

    def test_result_shape(self):
        reader = ImageReader(self._tests_dir)
        x, y = reader.read()
        self.assertEqual((6, 3, 255, 255), x.shape)
        self.assertEqual((6, 5), y.shape)

    def test_result_shape_label_format(self):
        reader = ImageReader(self._tests_dir, {"label_format": "label"})
        x, y = reader.read()
        self.assertEqual((6, 3, 255, 255), x.shape)
        self.assertEqual((6,), y.shape)

    def test_batch_read_when_no_remainder(self):
        reader = ImageReader(self._tests_dir, {"batch_size": 2})
        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 5), y.shape)

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 5), y.shape)

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 5), y.shape)
        self.assertFalse(reader.has_next())

    def test_batch_read_when_remainder(self):
        reader = ImageReader(self._tests_dir, {"batch_size": 5})
        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((5, 3, 255, 255), x.shape)
        self.assertEqual((5, 5), y.shape)

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((1, 3, 255, 255), x.shape)
        self.assertEqual((1, 5), y.shape)

    def test_batch_read_ensure_all_files_were_read(self):
        mock_img_arr = numpy.ndarray((3, 255, 255))

        mock_files = []
        mock_labels = {}
        mock_classes = set()
        for i in range(0, 25):
            file_name = "img_{}.jpg".format(i)
            mock_files.append(pathlib.Path(file_name))
            mock_labels[file_name] = int(i)
            mock_classes.add(int(i))

        with mock.patch.object(ImageReader, '_list_and_validate', return_value=mock_files):
            with mock.patch.object(ImageReader, '_read_labels_and_classes', return_value=(mock_labels, mock_classes)):
                with mock.patch.object(ImageReader, '_img_to_arr', return_value=mock_img_arr):
                    options = {"batch_size": 3}
                    reader = ImageReader(self._tests_dir, options)
                    while reader.has_next():
                        x, y = reader.read()
                        for label_vector in y:
                            label = label_vector.tolist().index(1)
                            del mock_labels["img_{}.jpg".format(label)]

                    self.assertFalse(reader.has_next())
                    self.assertTrue(not mock_labels)

    def test_result_order(self):
        pixels = self._expected_pixels()
        reader = ImageReader(self._tests_dir, {"normalize": False})
        x, y = reader.read()
        for i in range(len(y)):
            label = y[i].tolist().index(1)  # in one-hot-encoding location of 1 should match the label

            first_five_pixels = x[i][0][0][:5]
            expected = pixels[label]
            if label == 1:
                self.assertTrue(numpy.array_equal(expected[0], first_five_pixels) or numpy.array_equiv(expected[1], first_five_pixels))
                continue
            self.assertTrue(numpy.array_equal(expected, first_five_pixels))

        self.assertEqual((6, 3, 255, 255), x.shape)
        self.assertEqual((6, 5), y.shape)

    def test_result_order_when_batch_read(self):
        pixels = self._expected_pixels()
        reader = ImageReader(self._tests_dir, {"normalize": False, "batch_size": 1})
        while reader.has_next():
            x, y = reader.read()
            label = y[0].tolist().index(1)  # in one-hot-encoding location of 1 should match the label
            first_five_pixels = x[0][0][0][:5]
            expected = pixels[label]
            if label == 1:
                self.assertTrue(numpy.array_equal(expected[0], first_five_pixels) or numpy.array_equiv(expected[1], first_five_pixels))
                continue
            self.assertTrue(numpy.array_equal(expected, first_five_pixels))
            self.assertEqual((1, 3, 255, 255), x.shape)
            self.assertEqual((1, 5), y.shape)

    @staticmethod
    def _expected_pixels():
        pixels = dict()
        pixels[0] = [0, 0, 0, 0, 0]
        pixels[1] = [[35, 31, 19, 32, 27], [250, 250, 249, 250, 250]]
        pixels[2] = [38, 33, 32, 39, 58]
        pixels[3] = [255, 255, 255, 255, 255]
        pixels[4] = [246, 246, 246, 246, 246]
        return pixels


if __name__ == '__main__':
    main()
