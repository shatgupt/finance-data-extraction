import os
import calendar
from importlib.machinery import SourceFileLoader
from pypdf import PdfReader, PdfWriter

# US Treasury Exchange Rates
exchange_rate = SourceFileLoader(
    "exchange_rate", os.path.dirname(__file__) + "/exchange_rate.py"
).load_module()

from exchange_rate import *

ExchangeRate.load_US_treasury_INR_rates()


def get_all_pdf_paths(directory):
    with os.scandir(directory) as it:
        return [entry.path for entry in it if entry.name.endswith(".pdf")]


def get_all_excel_paths(directory):
    with os.scandir(directory) as it:
        return [entry.path for entry in it if entry.name.endswith(".xlsx")]


def get_last_date_of_month(date):
    last_day = calendar.monthrange(date.year, date.month)[1]
    return date.replace(day=last_day)


def get_pdf_reader(pdf_path, password=None):
    # print("Reading ", pdf_path)
    reader = PdfReader(pdf_path)

    if reader.is_encrypted:
        if password is None:
            raise Exception("Password required to read pdf: " + pdf_path)
        reader.decrypt(password)

    return reader


def write_pdf(pdf_reader, output_path):
    writer = PdfWriter()
    # Add all pages to the writer
    for page in pdf_reader.pages:
        writer.add_page(page)

    # Save the new PDF to a file
    with open(output_path, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    from datetime import date

    print(get_last_date_of_month(date.today()))
    print(ExchangeRate.get_inr_rate(date.today()))
