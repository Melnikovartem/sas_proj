import requests

import os
import re
import random
import string

from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, default='links')
parser.add_argument("-o", "--output", type=str, default='html_pages')
parser.add_argument("--hard", action='store_true')

args = parser.parse_args()

if not os.path.isdir(args.output):
    os.mkdir(args.output)

with open(args.input, 'r') as links:
    for link in tqdm(links, desc="downloading"):

        file_name = re.search(".*EventId=(.*)$", link)

        if not file_name:
            file_name = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(27))
        else:
            file_name = file_name.group(1)

        file_path = f"{ args.output}/{file_name}.html"

        if os.path.isfile(file_path) and not args.hard:
            continue

        page = requests.get(link.strip("\n"))

        with open(file_path, "wb") as file:
            file.write(page.content)
