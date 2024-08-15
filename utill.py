import json
import os
from PyPDF2 import PdfReader

BANK_SIZES = json.load(open("bankSizes.json"))
SUCCESS = "✅"
FAIL = "❌"

BANK_TEMPLATES = json.load(open("template.json"))


def compare(data):
    result = dict(map(lambda x: (x['name'], FAIL), BANK_TEMPLATES))
    for bank in BANK_TEMPLATES:
        bank = bank.copy()
        name = bank.pop("name")
        data_size = data["size"]

        template_data_match = all(data.get(k) == v for k, v in bank.items())
        size_match = int(data_size) in BANK_SIZES[name]

        result[name] = SUCCESS if template_data_match and size_match else FAIL

    return "\n".join(map(lambda bank_result: f"{bank_result[0]} {bank_result[1]}", result.items()))

