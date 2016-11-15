from FOIAbilityDoc import FOIAbilityDoc
from FOIAbilityPDF import FOIAbilityPDF
from FOIAbilityText import FOIAbilityText

from examples.extract_text_per_page import extract_text_per_page
from examples.map_NER_per_page import map_NER_per_page
from examples.download_ocr_text_per_page import download_ocr_text_per_page
from examples.upload_pdf_to_documentcloud import upload_pdf_to_documentcloud
from examples.find_word_frequencies_per_page import find_word_frequencies_per_page
from examples.get_bag_of_words_per_page import get_bag_of_words_per_page
from examples.parse_metadata_from_pdf import parse_metadata_from_pdf
from examples.check_for_gibberish import check_for_gibberish
#from examples.extract_attachment_from_raw_email import extract_attachment_from_raw_email
#from examples.chart_email_chain_over_time import chart_email_chain_over_time
#from examples.export_incomplete_ocr_to_google_drive import export_incomplete_ocr_to_google_drive
#from examples.import_completed_text_from_google_drive import import_completed_text_from_google_drive

from utils import get_credentials, setup_schema
from vars import *

TEST_PDF = os.path.join(DATA_DIR, "rindfleisch_a90d1239f1626171d2e5cb759e8891d6_11.pdf")
TEST_EMAIL_PDF = os.path.join(DATA_DIR, "fpf_foia_emails.pdf")
TEST_PDF_DOCUMENTCLOUD_ID = ""
TEST_TEXT_BLOB = "I complained to Microsoft about Bill Gates and Oprah"

def test_extract_text_per_page():
	first_page = extract_text_per_page(TEST_PDF, 1)
	print first_page[0]
	print "*************\n"

	second_page = extract_text_per_page(first_page[1], 2)
	print second_page[0]
	print "*************\n"

def test_ner_per_page():
	page_text = extract_text_per_page(TEST_PDF, 1)[0]
	ner = map_NER_per_page(page_text)

	print ner

def test_find_word_frequencies_per_page():
	page_text = extract_text_per_page(TEST_PDF, 1)[0]
	word_frequencies = find_word_frequencies_per_page(page_text, os.path.join(MISC_DIR, "stopwords.json"))

	print word_frequencies

def test_get_bag_of_words_per_page():
	page_text = extract_text_per_page(TEST_PDF, 1)[0]
	bag_of_words = get_bag_of_words_per_page(page_text, os.path.join(MISC_DIR, "stopwords.json"))

	print bag_of_words

def test_download_ocr_text_per_page():
	print download_ocr_text_per_page(TEST_PDF_DOCUMENTCLOUD_ID, 1, get_credentials('Documentcloud'))

def test_upload_pdf_to_documentcloud():
	print upload_pdf_to_documentcloud(TEST_PDF, get_credentials('Documentcloud'))

def test_parse_metadata_from_pdf():
	print parse_metadata_from_pdf(TEST_EMAIL_PDF)

def test_check_for_gibberish():
	is_english = extract_text_per_page(TEST_PDF, 1)[0]
	print check_for_gibberish(is_english)

	is_gibberish = extract_text_per_page(TEST_EMAIL_PDF, 10)[0]
	print check_for_gibberish(is_gibberish)

def test_get_credentials():
	print get_credentials('Documentcloud')

def test_setup_schema():
	print "SETTING UP SCHEMA"
	setup_schema()

def test_create_doc():
	doc = FOIAbilityDoc(file_path=TEST_PDF)
	doc.emit(pretty=True)
	doc.delete()

def test_create_pdf():
	pdf = FOIAbilityPDF(file_path=TEST_PDF)
	pdf.emit(pretty=True)
	pdf.delete()

def test_create_text():
	text = FOIAbilityText(text_stream=TEST_TEXT_BLOB)
	text.delete()

def test_create_email():
	pdf = FOIAbilityPDF(file_path=TEST_EMAIL_PDF)
	pdf.emit(pretty=True)
	pdf.delete()

if __name__ == "__main__":
	#test_get_credentials()
	#test_extract_text_per_page()
	#test_check_for_gibberish()
	#test_ner_per_page()
	#test_upload_pdf_to_documentcloud()
	#test_download_ocr_text_per_page()
	#test_find_word_frequencies_per_page()
	#test_get_bag_of_words_per_page()
	#test_parse_metadata_from_pdf()
	test_setup_schema()
	#test_create_doc()
	#test_create_pdf()
	#test_create_email()
	#test_create_text()
	#test_get_doc_by_id()
	#test_delete_doc()