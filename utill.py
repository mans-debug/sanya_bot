import json, re

BANK_SIZES = json.load(open("static/bankSizes.json"))
BANK_TEMPLATES = json.load(open("static/template.json"))
BANK_TRANSACTION_DATE_REGEX = json.load(open("static/bankTransactionDateRegex.json"))


def compare(data):
    result = dict(map(lambda x: (x['name'], False), BANK_TEMPLATES))
    for bank in BANK_TEMPLATES:
        bank = bank.copy()
        name = bank.pop("name")
        data_size = data["size"]

        template_data_match = all(data.get(k) == v for k, v in bank.items())
        size_match = int(data_size) in BANK_SIZES[name]

        result[name] = template_data_match and size_match

    # return "\n".join(map(lambda bank_result: f"{bank_result[0]} {bank_result[1]}", result.items()))
    return result


def extract_transaction_date(pdf_text, bank_name):
    try:
        if bank_name is None:
            return "-"
        return next(re.finditer(BANK_TRANSACTION_DATE_REGEX[bank_name], pdf_text)).group()
    except Exception as e:
        print(e)
        return "-"

