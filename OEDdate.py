import csv
import re
import time

import requests
from bs4 import BeautifulSoup
import json


def main():
    print('Beginning text dating process.')

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

                resp = requests.get(url, headers=headers)

                js = bytes()

                for chunk in resp.iter_content(chunk_size=512 * 1024):
                    js += chunk

                js = js.decode('utf-8')

                representation = json.loads(js)

                if len(representation) > 0:
                    if 'daterange' in representation[0][0]:
                        print('[{0}]: {1}'.format(word, representation[0][0]['daterange']['start']))
                        output_writer.writerow([word, representation[0][0]['daterange']['start']])
                        csv_out.flush()
                else:
                    print('[{0}]: {1}'.format(word, 'No date'))
                    output_writer.writerow([word, '0'])

if __name__ == "__main__":
    main()