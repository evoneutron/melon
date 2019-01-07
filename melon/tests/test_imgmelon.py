import unittest

import melon


class TestImageMelon(unittest.TestCase):

    def setUp(self):
        self.melon = melon.ImageMelon()

    def test_result_shape(self):
        result_arr = self.melon.interpret("./resources/images")
        self.assertEqual((2, 3, 255, 255), result_arr.shape)


if __name__ == '__main__':
    unittest.main()
