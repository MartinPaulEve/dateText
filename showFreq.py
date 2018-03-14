import re
from collections import OrderedDict
from collections import Counter


def main():
    print('Beginning text frequency process.')

    un_dict = {}
    ret_dict = OrderedDict()

    with open('CA_Words.txt', 'r') as file_one:
        file_one_contents = file_one.read()
        # standardise curly quotes
        file_one_contents = re.sub('\’', '\'', file_one_contents)
        file_one_contents = re.sub('[^a-zA-Z\s]*', '', file_one_contents)
        file_one_contents = re.sub('[\n\r]', ' ', file_one_contents)
        file_one_contents = file_one_contents.lower()

        file_one_split = list(set(file_one_contents.split(' ')))
        file_one_counts = Counter(file_one_contents.split(' '))

        word_count = len(file_one_contents.split(' '))

        with open('w_mag_2004.txt', 'r') as file_two:
            file_two_contents = file_two.read()
            # remove COCA numbering
            ##2009192
            file_two_contents = re.sub('##\d{7}', '', file_two_contents)
            # standardise curly quotes
            file_two_contents = re.sub('\’', '\'', file_two_contents)

            # merge COCA quoted bits
            file_two_contents = re.sub(' \'', '\'', file_two_contents)
            file_two_contents = re.sub('[^a-zA-Z\s]*', '', file_two_contents)


            file_two_contents = re.sub('[\n\r]', ' ', file_two_contents)
            file_two_contents = file_two_contents.lower()

            file_two_split = list(set(file_two_contents.split(' ')))
            file_two_counts = Counter(file_two_contents.split(' '))

            for word in file_one_split:
                if word in file_two_split:
                    un_dict[word] = file_two_counts[word]
                else:
                    un_dict[word] = 0

            ret_dict = OrderedDict(sorted(un_dict.items()))

            for k, v in ret_dict.items():
                print("{0}, {1}".format(k, v))

            word_count_one = len(file_two_contents.split(' '))
            word_count = len(file_two_contents.split(' '))
            print(word_count)

if __name__ == "__main__":
    main()
