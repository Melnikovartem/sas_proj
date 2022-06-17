import re
from collections import defaultdict

months = {
    "январь": "01",
    "января": "01",
    "февраль": "02",
    "февраля": "02",
    "март": "03",
    "марта": "03",
    "апрель": "04",
    "апреля": "04",
    "май": "05",
    "мая": "05",
    "июнь": "06",
    "июня": "06",
    "июль": "07",
    "июля": "07",
    "август": "08",
    "августа": "08",
    "сентябрь": "09",
    "сентября": "09",
    "октябрь": "10",
    "октября": "10",
    "ноябрь": "11",
    "ноября": "11",
    "декабрь": "12",
    "декабря": "12",
}


def parse_name(line):
    split = ":"
    if not split in line:
        split = "\t"
    if not split in line:
        split = " - "
    if not split in line:
        return None
    return line.split(split)[-1].strip()


def parse_address(line):
    split = ":"
    post_index = re.search(r"\d{6},?[ ]?", line)
    if post_index:
        split = post_index[0]
    return line.split(split)[-1].strip()


def parse_ogrn(line):
    res = re.findall(r"\d{13}", line)
    return res[0] if len(res) > 0 else None


def parse_iin(line):
    res = re.findall(r"\d{10}", line)
    return res[0] if len(res) > 0 else None


def parse_date(line):
    line = ''.join(line.split()).replace("«", "").replace("»", "")
    found = re.findall(
        r'(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})', line)
    if len(found):
        return ".".join(found[0])
    found = re.findall(
        r'(3[01]|[12][0-9]|0?[1-9])(«?[а-я]{3,8}»?)((?:19|20)\d{2})', line)
    if len(found):
        date = list(found[0])
        month = date[1].lower()
        if month in months:
            date[1] = months[month]
        else:
            print("ERROR: unknown month:", month)
        return ".".join(date)
    return None


def parse_text(text):
    data = defaultdict(lambda: None)
    lines = text.split("\n")
    for line in lines:
        if re.match("^1\.\d", line):
            # на случай если придерживаются стандартного порядка
            if re.match("^1.1", line) and not data["name_long"]:
                data["name_long"] = parse_name(line)
            elif re.match("^1.2", line):
                data['adress'] = parse_address(line)
            elif re.match("^1.3", line):
                data['orgn'] = parse_ogrn(line)
            elif re.match("^1.4", line):
                data['inn'] = parse_iin(line)
            elif re.match("^1.7", line):
                data["date"] = parse_date(line)

    req_keys = ["adress", "ogrn", "inn", "date"]
    broken = False
    for key in req_keys:
        if not data[key]:
            broken = True
            break

    if broken:
        # fixing broken data

        no_date = not data["date"]

        for line_id in range(len(lines)):
            line = lines[line_id].strip()
            next_line = ""
            if len(lines) > line_id + 1:
                next_line = lines[line_id + 1].strip()

            if re.match("^1\.\d", line):
                if not data['name_long'] and re.match("^1.1", line):
                    if not re.match("^1.", next_line) and next_line:
                        data["name_long"] = next_line
                    else:
                        data["name_long"] = line

                if not data['orgn'] and ("огрн" in line.lower()):
                    data['orgn'] = parse_ogrn(line)
                    if not data['orgn']:
                        data['orgn'] = parse_ogrn(next_line)

                if not data['inn'] and ("инн" in line.lower()):
                    data['inn'] = parse_iin(line)
                    if not data['inn']:
                        data['inn'] = parse_iin(next_line)

                if not data['adress'] and "адрес" in line.lower():
                    data['adress'] = parse_iin(line)

                if no_date and "дата" in line.lower():
                    # хотим последнюю валидную дату в секции "общая информация"
                    data["date"] = parse_date(line)
                    if not data['date']:
                        data['date'] = parse_date(next_line)

    return data
