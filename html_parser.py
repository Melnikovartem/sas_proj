from bs4 import BeautifulSoup
import sqlite3

from parser_base import parse_text
from parser_smart import check_divident, check_audit, check_board

import os
import re

from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, default='html_pages')
parser.add_argument("-d", "--database", type=str, default='results.db')

args = parser.parse_args()

sqlite_connection = sqlite3.connect(args.database)
cursor = sqlite_connection.cursor()

for file_name in tqdm(os.listdir(args.input), desc="parsing"):
    file_path = f"{args.input}/{file_name}"
    if not os.path.isfile(file_path) or not re.match(".*\.html", file_name):
        continue

    with open(file_path, 'r') as html_file:

        soup = BeautifulSoup(html_file.read(), 'html.parser')

        text_to_parse = list(soup.find_all(id="cont_wrap")
                             [0].children)[3].get_text()
        data = parse_text(text_to_parse)

        if not data["inn"]:
            continue

        infoblock = soup.find_all(class_="infoblock")[0]

        data["eventId"] = file_name[:-5]

        data["topic"] = infoblock.find_all("h4")[0].get_text()
        data["name_short"] = infoblock.find_all("h2")[0].get_text()

        data["dividend"] = check_divident(text_to_parse)
        data["board_names"] = check_board(text_to_parse)

        audit_results = check_audit(text_to_parse, data["inn"])
        if audit_results:
            data["audit_inn"] = audit_results["audit_inn"]
            data["audit_name"] = audit_results["audit_name"]
            data["audit_type"] = audit_results["audit_type"]

        keys = ["eventId", "name_short", "name_long",
                "adress", "inn", "orgn", "topic", "date", "dividend", "board_names", "audit_inn", "audit_name", "audit_type"]
        for key in keys:
            if type(data[key]) == str:
                info = data[key].replace("'", " ")
                data[key] = f"'{info}'"
            else:
                data[key] = "NULL"
        cursor.execute(f"""
            INSERT INTO parsed_results
            ({",".join(keys)})  VALUES
            ({",".join([data[key] for key in keys])})
        """)

sqlite_connection.commit()
cursor.close()
