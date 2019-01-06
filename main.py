from imgmelon import Interpreter


def main():
    options = {"normalize": True}
    interpreter = Interpreter(options)

    result = interpreter.interpret("/Users/rjuga255/PycharmProjects/melon/source_sample")
    print(result.shape)


if __name__ == "__main__":
    main()
