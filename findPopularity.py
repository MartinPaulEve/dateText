import csv
import re
import time

import requests
from bs4 import BeautifulSoup


def main():
    print('Beginning text popularity assessment using Merriam Webster.')

    # build a regular expression pattern that can be re-used to search for popularity expressions in
    # Merriam Webster entries
    popularity_pattern = re.compile('(Top|Bottom) \d+% of words')

    # build a headers dictionary that looks like a real computer and not a machine
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/39.0.2171.95 Safari/537.36'}

    with open('outfile.txt', 'r') as text:
        with open('popularity_outfile.csv', 'w') as csv_out:
            # create a csv-writer object
            output_writer = csv.writer(csv_out, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

            # read the input text line by line into the text_list variable
            text_list = text.readlines()

            count = 0

            # iterate over the words
            for word in text_list:
                count += 1

                # remove any trailing newline characters
                word = word.strip('\n')

                # create a string of a URL that
                url = 'http://stats.merriam-webster.com/pop-score-redesign.php?word={0}&id=popularity-score'.format(word)

                if count == 20:
                    time.sleep(2000)
                    count = 0
                else:
                    # wait 10 seconds so that we do not hammer the dictionary.com server
                    time.sleep(10)

                # Get the fetched page
                fetched_page = requests.get(url, headers=headers).text

                # test whether dictionary.com has a usage section
                has_usage = popularity_pattern.search(fetched_page)

                if has_usage:

                    # look through the document for a span tag where the text matches the date_pattern
                    result = popularity_pattern.search(fetched_page)

                    if result:
                        popularity = result.group()

                        # write the found date to the CSV
                        print('[{0}]: {1}'.format(word, popularity))
                        output_writer.writerow([word, popularity])
                    else:
                        write_failure(output_writer, word)
                else:
                    write_failure(output_writer, word)

                    # write the output to the file in case we crash
                csv_out.flush()

    print('Done.')


def write_failure(output_writer, word):
    # write a blank row to the output CSV indicating that we found no date
    print('[{0}]: Found no popularity'.format(word))
    output_writer.writerow([word, 'NO POPULARITY'])

if __name__ == "__main__":
    main()