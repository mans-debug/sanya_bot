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


def create_data(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_file = PdfReader(file)
        pdf_info = pdf_file.metadata
        version = pdf_file.pdf_header

    data = {
        "size": os.path.getsize(pdf_path) // 1024,
        "ver": version[5:8],
        "creator": pdf_info.get('/Creator'),
        "producer": pdf_info.get('/Producer'),
    }
    return compare(data)


if __name__ == "__main__":
    dir_path = "sample_pdf/"
    pdfs = os.listdir(dir_path)
    for pdf in pdfs:
        print(create_data(dir_path + pdf), sep="\n\n")
