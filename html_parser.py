from bs4 import BeautifulSoup

import os
import re

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, default='html_pages')
parser.add_argument("-o", "--output", type=str, default='results.db')

args = parser.parse_args()

for file_name in os.listdir(args.input):
    file_path = f"{args.input}/{file_name}"
    if not os.path.isfile(file_path) or not re.match(".*\.html", file_name):
        continue

    with open(file_path, 'r') as html_file:

        soup = BeautifulSoup(html_file.read(), 'html.parser')

        infoblock = soup.find_all(class_="infoblock")[0]

        data = {}

        data["topic"] = infoblock.find_all("h4")[0].get_text()

        data["short_name"] = infoblock.find_all("h2")[0].get_text()

        text_to_parse = list(soup.find_all(id="cont_wrap")
                             [0].children)[3].get_text()

        print(text_to_parse)
