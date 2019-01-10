import time

from melon import ImageLoader


def main():
    start_time = time.time()
    options = {"normalize": False}
    loader = ImageLoader(options)
    x, y = loader.read("../melon/tests/resources/temp_resource")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
