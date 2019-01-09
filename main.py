import time

from melon import ImageMelon


def main():
    start_time = time.time()
    options = {"normalize": False}
    melon = ImageMelon(options)
    x, y = melon.interpret("../melon/tests/resources/temp_resource")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
