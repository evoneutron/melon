from melon import ImageReader


def main():
    loader = ImageReader("../melon/tests/resources/temp_resource")
    x, y = loader.read()


if __name__ == "__main__":
    main()
