import sqlite3

import os

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--database", type=str, default='results.db')
parser.add_argument("--hard", action='store_true')

args = parser.parse_args()

if args.hard and os.path.exists(args.database):
    os.remove(args.database)

if not os.path.exists(args.database):
    sqlite_connection = sqlite3.connect(args.database)
    sqlite_create_table_query = '''CREATE TABLE parsed_results (
                                    id INTEGER PRIMARY KEY,
                                    eventId TEXT NOT NULL,
                                    name_short text NOT NULL,
                                    name_long TEXT NOT NULL,
                                    topic TEXT NOT NULL);'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
