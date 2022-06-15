import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, default='links')

args = parser.parse_args()

with open(args.input, 'w') as links:
    links.write(
        "https://e-disclosure.ru/portal/event.aspx?EventId=1GwHbOyvWUqOt-CgzoqAroQ-B-B")
