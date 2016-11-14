from PyPDF2 import PdfFileReader

from FOIAbilityDoc import FOIAbilityDoc
from FOIAbilityText import FOIAbilityText
from examples.extract_text_per_page import extract_text_per_page
from examples.download_orc_text_per_page import download_orc_text_per_page

from utils import get_credentials
from vars import MIME_TYPES

class FOIAbilityPDF(FOIAbilityDoc):
	MODES = MIME_TYPES['pdf']['eval_modes']

	def __init__(self, file_path=None, id=None):
		FOIAbilityDoc.__init__(self, file_path=file_path, id=id)

	def create(self):
		if not FOIAbilityDoc.create(self):
			return False

		try:
			self.pdf_reader = PdfFileReader(open(self.obj['file_path'], 'rb'))
		except Exception as e:
			print "FOIAbilityPDF ERROR: could not load PDF from file_path"
			print e, type(e)
			return False

		return self.evaluate_text()

	def evaluate_text(self, mode=MODES['PyPDF']):
		try:
			# get number of pages
			self.obj['num_pages'] = self.pdf_reader.getNumPages()

			# keep tally of how many pages actually have text in them
			self.obj['num_pages_with_embedded_text'] = 0

			# for each page, attempt to extract text
			for page in xrange(self.obj['num_pages']):
				text = None
				
				if mode == MODES['PyPDF']:
					try:
						text, self.pdf_reader = extract_text_per_page(self.pdf_reader, page)
					except Exception as e:
						print "FOIAbilityPDF WARN: could not get text from page (mode PyPDF)"
						print e, type(e)
						continue

				if mode == MODES['Documentcloud']:
					try:
						text = download_orc_text_per_page(page, get_credentials('Documentcloud'))
					except Exception as e:
						print "FOIAbilityPDF WARN: could not get text from page (mode Documentcloud)"
						print e, type(e)
						continue
				
				# if page doesn't have text in it, move on
				if text is None or len(text) == 0:
					continue

				# increment tally
				self.obj['num_pages_with_embedded_text'] = (self.obj['num_pages_with_embedded_text'] + 1)

				# make indexible text object for text
				try:
					self.link_doc(FOIAbilityText(text_stream=text, parent_id=self.obj['id']).obj['id'])
				except Exception as e:
					print "FOIAbilityPDF WARN: could not create text object from page"
					print e, type(e)
					continue

				if page >= 5:
					break

			return True
		except Exception as e:
			print "FOIAbilityPDF ERROR: could not get number of pages in this PDF"
		
		return False