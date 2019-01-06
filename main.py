from melon import ImageMelon


def main():
    options = {"normalize": True}
    melon = ImageMelon(options)
    result = melon.interpret("../PycharmProjects/melon/source_sample")
    print(result.shape)


if __name__ == "__main__":
    main()
