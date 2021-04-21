"""
Author: Denyson Grellert
"""

import pdfminer.high_level
from unicodedata import normalize

def pdf2string(file, pages=None):
	return normalize("NFKD", pdfminer.high_level.extract_text(file, page_numbers=pages))

def pdf2txt(file, name, pages=None):
	text = pdf2string(file, pages)
	with open(name, 'w') as f:
		f.write(text)

def txt2string(file):
	with open(file, 'r') as f:
		string = f.read()
	return string
