import csv
import re
import time

import requests
from bs4 import BeautifulSoup


def main():
    print('Beginning text dating process.')

    # build a regular expression pattern that can be re-used to search for usage expressions in dictionary.com pages
    # this pattern is designed to match a date range (e.g. 1900-1905)
    date_pattern = re.compile('\d{4}-\d{4}')

    date_before_pattern = re.compile('\d{3,4};')

    # build a regular expression pattern that can be used to see whether there is a "word usage" section
    usage_pattern = re.compile('Origin of')

    # build a headers dictionary that looks like a real computer and not a machine
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/39.0.2171.95 Safari/537.36'}

    with open('infile.txt', 'r') as text:
        with open('dated_outfile.csv', 'w') as csv_out:

            # create a csv-writer object
            output_writer = csv.writer(csv_out, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

            # read the input text line by line into the text_list variable
            text_list = text.readlines()

            # iterate over the words
            for word in text_list:
                # remove any trailing newline characters
                word = word.strip('\n')

                # create a string of a URL that
                url = 'http://www.dictionary.com/browse/{0}?s=t'.format(word)

                # wait 10 seconds so that we do not hammer the dictionary.com server
                time.sleep(10)

                # parse the fetched URL into a BeautifulSoup object for XML handling
                soup_object = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')

                # test whether dictionary.com has a usage section
                has_usage = (len(soup_object.body.findAll(text=usage_pattern)) > 0)

                if has_usage:
                    # look through the document for a span tag where the text matches the date_pattern
                    xml = soup_object.find('span', text=date_pattern)

                    if xml:
                        date_range = xml.getText()

                        # write the found date to the CSV
                        print('[{0}]: {1}'.format(word, date_range))
                        output_writer.writerow([word, date_range])

                    else:
                        # see if this is a "before 900"-type date
                        xml = soup_object.find('span', text=date_before_pattern)

                        if xml:
                            date_range = xml.getText()

                            # write the found date to the CSV
                            print('[{0}]: {1}'.format(word, date_range))
                            output_writer.writerow([word, date_range])
                        else:
                            write_failure(output_writer, word)
                else:
                    write_failure(output_writer, word)

                # write the output to the file in case we crash
                csv_out.flush()

    print('Done.')


def write_failure(output_writer, word):
    # write a blank row to the output CSV indicating that we found no date
    print('[{0}]: Found no date'.format(word))
    output_writer.writerow([word, 'NO DATE'])


if __name__ == "__main__":
    main()
