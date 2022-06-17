from bs4 import BeautifulSoup
import sqlite3

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

        infoblock = soup.find_all(class_="infoblock")[0]

        data = {}

        data["eventId"] = file_name[:-5]

        data["topic"] = infoblock.find_all("h4")[0].get_text()
        data["name_short"] = infoblock.find_all("h2")[0].get_text()

        text_to_parse = list(soup.find_all(id="cont_wrap")
                             [0].children)[3].get_text()

        print(text_to_parse)

        dividend = "вопрос не поднимался"
        audi_sql = "NULL, NULL, NULL"

        cursor.execute(f"""
            INSERT INTO parsed_results
            (eventId, name_short, name_long, adress, inn, orgn, topic, date, audit_inn, audit_name, audit_type, board_names, dividend)  VALUES
            ('{data["eventId"]}',
            '{data["name_short"]}',
            '{data["name_long"]}',
            '{data["adress"]}',
            '{data["inn"]}',
            '{data["orgn"]}',
            '{data["topic"]}',
            '{data["date"]}',
            {audi_sql},
            {board_names or "NULL"},
            {dividend}
            )
        """)

sqlite_connection.commit()
cursor.close()
