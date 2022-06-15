import requests
from bs4 import BeautifulSoup

page = requests.get(
    "https://e-disclosure.ru/portal/event.aspx?EventId=1GwHbOyvWUqOt-CgzoqAroQ-B-B")


soup = BeautifulSoup(page.content, 'html.parser')

infoblock = soup.find_all(class_="infoblock")[0]


data = {}

data["topic"] = infoblock.find_all("h4")[0].get_text()

data["short_name"] = infoblock.find_all("h2")[0].get_text()

text_to_parse = list(soup.find_all(id="cont_wrap")[0].children)[3].get_text()

print(content)
