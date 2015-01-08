import sys

__author__ = 'gurjyan'


class Decomposer:

    def __init__(self, sentence):
        while len(sentence) % 4 != 0:
            sentence += " "
        f1 = open("../engines/Data/d1.txt", "wb")
        f2 = open("../engines/Data/d2.txt", "wb")
        f3 = open("../engines/Data/d3.txt", "wb")
        f4 = open("../engines/Data/d4.txt", "wb")
        i = -1
        while i < len(sentence):
            i += 1
            if i < len(sentence):
                f1.write(sentence[i])

            i += 1
            if i < len(sentence):
                f2.write(sentence[i])

            i += 1
            if i < len(sentence):
                f3.write(sentence[i])

            i += 1
            if i < len(sentence):
                f4.write(sentence[i])

        f1.close()
        f2.close()
        f3.close()
        f4.close()


def main(sent):
    Decomposer(sent)

if __name__ == '__main__':
    main(sys.argv[1])


