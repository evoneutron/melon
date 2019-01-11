import pathlib
from unittest import TestCase, mock, main

import numpy

from melon import ImageReader


class ImageReaderTestCase(TestCase):

    def test_result_shape(self):
        self.reader = ImageReader("tests/resources/images")
        x, y = self.reader.read()

        self.assertEqual((5, 3, 255, 255), x.shape)
        self.assertEqual(5, y.shape[0])

    def test_batch_read(self):
        options = {"batch_size": 2}
        reader = ImageReader("tests/resources/images", options)
        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual(2, y.shape[0])

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual(2, y.shape[0])

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((1, 3, 255, 255), x.shape)
        self.assertEqual(1, y.shape[0])
        self.assertFalse(reader.has_next())

    def test_batch_read_ensure_all_files_were_read(self):
        mock_img_arr = numpy.ndarray((3, 255, 255))

        mock_files = []
        mock_labels = {}
        for i in range(0, 25):
            file_name = "img_{}.jpg".format(i)
            mock_files.append(pathlib.Path(file_name))
            mock_labels[file_name] = int(i)

        with mock.patch.object(ImageReader, '_list_and_validate', return_value=mock_files):
            with mock.patch.object(ImageReader, '_read_labels', return_value=mock_labels):
                with mock.patch.object(ImageReader, '_img_to_arr', return_value=mock_img_arr):
                    options = {"batch_size": 3}
                    reader = ImageReader("tests/resources/images", options)
                    while reader.has_next():
                        x, y = reader.read()
                        for label in y:
                            del mock_labels["img_{}.jpg".format(label)]

                    self.assertFalse(reader.has_next())
                    self.assertTrue(not mock_labels)


if __name__ == '__main__':
    main()
