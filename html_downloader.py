import requests

import os
import re
import random
import string

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, default='links')
parser.add_argument("-o", "--output", type=str, default='html_pages')

args = parser.parse_args()

if not os.path.isdir(args.output):
    os.mkdir(args.output)

with open(args.input, 'r') as links:
    for link in links:
        page = requests.get(link.strip("\n"))

        file_name = re.search(".*EventId=(.*)$", link)

        if not file_name:
            file_name = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(27))
        else:
            file_name = file_name.group(1)

        file_path = f"{ args.output}/{file_name}.html"

        with open(file_path, "wb") as file:
            file.write(page.content)
