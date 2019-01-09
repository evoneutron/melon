import unittest

import melon

from melon.imgmelon_denominations import Denominations as denom


class TestImageMelon(unittest.TestCase):

    def setUp(self):
        options = {denom.num_threads: 1}
        self.melon = melon.ImageMelon(options)

    def test_result_shape(self):
        x, y = self.melon.interpret("./resources/images")

        self.assertEqual((4, 3, 255, 255), x.shape)
        self.assertEqual(4, y.shape[0])


if __name__ == '__main__':
    unittest.main()
