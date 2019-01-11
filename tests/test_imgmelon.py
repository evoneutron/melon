import pathlib
from unittest import TestCase, mock, main

import numpy as np

from melon import ImageReader


class TestImageMelon(TestCase):

    def test_result_shape(self):
        self.reader = ImageReader("./resources/images")
        x, y = self.reader.read()

        self.assertEqual((5, 3, 255, 255), x.shape)
        self.assertEqual(5, y.shape[0])

    def test_batch_read(self):
        mock_img_arr = np.ndarray((3, 255, 255))

        files_count = 65
        file_list = []
        for i in range(files_count):
            file_list.append(pathlib.Path("img_{}.jpg".format(i)))

        with mock.patch.object(ImageReader, '_list_and_validate', return_value=file_list):
            with mock.patch.object(ImageReader, '_ImageReader__img_to_arr', return_value=mock_img_arr):
                options = {"batch_size": 30}
                reader = ImageReader("", options)

                self.assertTrue(reader.has_next())
                x, y = reader.read()
                self.assertEqual((30, 3, 255, 255), x.shape)
                self.assertEqual(30, y.shape[0])

                self.assertTrue(reader.has_next())
                x, y = reader.read()
                self.assertEqual((30, 3, 255, 255), x.shape)
                self.assertEqual(30, y.shape[0])

                self.assertTrue(reader.has_next())
                x, y = reader.read()
                self.assertEqual((5, 3, 255, 255), x.shape)
                self.assertEqual(5, y.shape[0])

                self.assertFalse(reader.has_next())

    def test_batch_read_ensure_all_files_were_read(self):
        mock_img_arr = np.ndarray((3, 255, 255))

        files_count = 65
        mock_files = []
        mock_labels = {}
        for i in range(0, files_count):
            file_name = "img_{}.jpg".format(i)
            mock_files.append(pathlib.Path(file_name))
            mock_labels[file_name] = int(i)

        with mock.patch.object(ImageReader, '_list_and_validate', return_value=mock_files):
            with mock.patch.object(ImageReader, '_ImageReader__read_labels', return_value=mock_labels):
                with mock.patch.object(ImageReader, '_ImageReader__img_to_arr', return_value=mock_img_arr):
                    options = {"batch_size": 30}
                    reader = ImageReader("", options)
                    while reader.has_next():
                        x, y = reader.read()
                        for label in y:
                            del mock_labels["img_{}.jpg".format(label)]

                    self.assertFalse(reader.has_next())
                    self.assertTrue(not mock_labels)


if __name__ == '__main__':
    main()
