import requests
from bs4 import BeautifulSoup

import re
from random import shuffle

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output", type=str, default='links')
parser.add_argument("-m", "--mode", type=str, default='random')
parser.add_argument("-a", "--amount", type=int, default=300)
parser.add_argument("--append", action='store_true')
parser.add_argument("--noshuffle", action='store_true')

parser.add_argument("--dateStart", type=str, default="01.01.2022")
parser.add_argument("--dateFinish", type=str, default="01.05.2022")
parser.add_argument("--text", type=str, default="")

args = parser.parse_args()

links = []

print(f"generating {args.amount} links to reports")

if args.mode == "random":
    search_link = "https://www.e-disclosure.ru/poisk-po-soobshheniyam"
    page = requests.post(search_link, json={
        "lastPageSize": 2147483647,
        "lastPageNumber": 1,
        "query": None,
        "queryEvent": None,
        "eventTypeTerm": None,
        "radView": 0,
        "dateStart": args.dateStart,
        "dateFinish": args.dateFinish,
        "textfieldEvent": args.text,
        "radReg": "FederalDistricts",
        "districtsCheckboxGroup": -1,
        "regionsCheckboxGroup": -1,
        "branchesCheckboxGroup": -1,
        "textfieldCompany": None
    })

    soup = BeautifulSoup(page.text, 'html.parser')
    results = soup.find_all("a")

    if not args.noshuffle:
        shuffle(results)

    for a_tag in results:
        link = a_tag.get('href')

        if re.match(r"https://www\.e-disclosure\.ru/portal/event\.aspx\?EventId=.*", link):
            links.append(link)

            if len(links) >= args.amount:
                break
else:
    raise NotImplementedError("wrong mode")

with open(args.output, 'a' if args.append else 'w') as links_file:
    if args.append:
        links_file.write("\n")
    links_file.write("\n".join(links))
