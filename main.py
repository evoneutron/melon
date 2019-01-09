from melon import ImageMelon

import time


def main():
    options = {"normalize": False,
               "num_threads": 8}
    melon = ImageMelon(options)

    start_time = time.time()
    x, y = melon.interpret("../melon/tests/resources/online_album_cut")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
