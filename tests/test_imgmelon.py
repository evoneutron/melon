import unittest

import melon


class TestImageMelon(unittest.TestCase):

    def setUp(self):
        self.loader = melon.ImageLoader()

    def test_result_shape(self):
        x, y = self.loader.read("./resources/images")

        self.assertEqual((4, 3, 255, 255), x.shape)
        self.assertEqual(4, y.shape[0])


if __name__ == '__main__':
    unittest.main()
