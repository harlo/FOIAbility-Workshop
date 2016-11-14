import os
from PyPDF2 import PdfFileReader

def extract_text_per_page(pdf, page_num):
	if type(pdf) is str and os.path.exists(pdf):
		pdf = PdfFileReader(open(pdf, 'rb'))

	try:
		return (pdf.getPage(page_num).extractText(), pdf)
	except Exception as e:
		print "extract_text_per_page ERROR"
		print e, type(e)

	return None