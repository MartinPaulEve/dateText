import csv
import re
import time

import requests
from bs4 import BeautifulSoup
import json


def main():
    print('Beginning text obsolence detection.')

    headers = {'Accept': 'application/json', 'app_id': '4a8d193f', 'app_key': '82ae76beacf86760039823b53d7c30e1'}
    base_url = 'https://oed-api-demo-2445581300291.apicast.io:443/oed/api/v0.0/words/?lemma='

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

                url = base_url + word

                try:
                    fetch_and_check(base_url, csv_out, headers, output_writer, url, word)
                except:
                    print("Waiting 20 seconds before retrying")
                    time.sleep(20)

                    try:
                        fetch_and_check(base_url, csv_out, headers, output_writer, url, word)
                    except:
                        print("Waiting 20 seconds before retrying")
                        time.sleep(20)

                        try:
                            fetch_and_check(base_url, csv_out, headers, output_writer, url, word)
                        except:
                            print("Waiting 20 seconds before retrying")
                            time.sleep(20)

                            try:
                                fetch_and_check(base_url, csv_out, headers, output_writer, url, word)
                            except:
                                print("FAILED at {0}".format(word))


def fetch_and_check(base_url, csv_out, headers, output_writer, url, word):
    resp = requests.get(url, headers=headers)
    js = bytes()
    for chunk in resp.iter_content(chunk_size=512 * 1024):
        js += chunk
    js = js.decode('utf-8')
    representation = json.loads(js)

    for dict_item in representation:
        for sub_item in dict_item:
            if 'daterange' in sub_item:
                print('[{0}]: {1}'.format(word, sub_item['daterange']['obsolete']))
                output_writer.writerow([word, sub_item['daterange']['obsolete']])
                csv_out.flush()
            else:
                print('[{0}]: {1}'.format(word, 'No data'))
                output_writer.writerow([word, 'No data'])


if __name__ == "__main__":
    main()