import re

from parser_base import parse_iin


def parse_name_audit(st):
    res = re.search(
        r"(ооо|ао|ип|фирма)\s*«?[^«»]*(ауд|конс|экспер|kpmg|ernst|кпмг|эрнст)[^«»]*»?", st.lower())
    if res:
        return res[0] if len(res[0]) < 50 else None
    return None


def parse_type_audit(st):
    res = None
    return None


def check_audit(text, company_inn):
    if not "аудит" in text.lower():
        return None

    data = {
        "audit_inn": None,
        "audit_name": None,
        "audit_type": None,
    }

    lines = text.split("\n")

    for line in lines:
        if not re.match("^1\.\d", line) and "инн" in line.lower() and not data["audit_inn"]:
            parsed_inn = parse_iin(line)
            if parsed_inn != company_inn:
                data["audit_inn"] = parsed_inn

        sts = line.split(".")

        for st in sts:
            if not data["audit_name"]:
                data["audit_name"] = parse_name_audit(st)
            if not data["audit_type"]:
                data["audit_type"] = parse_type_audit(st)

    if not data["audit_name"] and not data["audit_type"]:
        data["audit_inn"] = None

    return data


def check_divident(text):
    ans = "вопрос не поднимался"
    lines = text.split("\n")
    for line in lines:
        if "дивиденд" in line:
            ans = "принято решение выплатить дивиденды"
        if ' не' in line.lower() and res['dividend_discuss'] and 'выпла' in line.lower():
            ans = "принято решение не выплачивать дивиденды"
    return ans


def check_board(text):
    return None
