import requests
from bs4 import BeautifulSoup

import re

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, default='links')
parser.add_argument("-m", "--mode", type=str, default='last')
parser.add_argument("-a", "--amount", type=int, default=300)

args = parser.parse_args()

links = []

if args.mode == "last":
    search_link = "https://www.e-disclosure.ru/poisk-po-soobshheniyam"
    page = requests.post(search_link, json={
        "lastPageSize": 2147483647,
        "lastPageNumber": 1,
        "query": None,
        "queryEvent": None,
        "eventTypeTerm": None,
        "radView": 0,
        "dateStart":  "17.05.2022",
        "dateFinish": "17.06.2022",
        "textfieldEvent": None,
        "radReg": "FederalDistricts",
        "districtsCheckboxGroup": -1,
        "regionsCheckboxGroup": -1,
        "branchesCheckboxGroup": -1,
        "textfieldCompany": None
    })

    soup = BeautifulSoup(page.text, 'html.parser')
    results = soup.find_all("a")

    for a_tag in results:
        link = a_tag.get('href')

        if re.match("https://www\.e-disclosure\.ru/portal/event\.aspx\?EventId=.*", link):
            links.append(link)

            if len(links) > args.amount:
                break

elif args.mode == "company":
    pass
else:
    raise NotImplementedError("wrong mode")

with open(args.input, 'w') as links_file:
    links_file.write("\n".join(links))
