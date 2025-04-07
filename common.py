# Common helpers
import re
from collections import namedtuple

def extract_three_digit_numbers(path):
    return re.findall(r'(?<!\d)\d{3}(?!\d)', str(path))

def extract_three_digits_after(path,after):
    return re.findall(after + r'(\d{3})', str(path))

SortedID = namedtuple("SortedID", ["provenance_id", "project_path", "confidence", "extra", "why"])
