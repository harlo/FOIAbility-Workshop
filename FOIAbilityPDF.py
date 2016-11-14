from PyPDF2 import PdfFileReader

from FOIAbilityDoc import FOIAbilityDoc
from FOIAbilityText import FOIAbilityText
from examples.extract_text_per_page import extract_text_per_page

class FOIAbilityPDF(FOIAbilityDoc):
	def __init__(self, file_path=None, id=None):
		FOIAbilityDoc.__init__(self, file_path=file_path, id=id)

	def create(self):
		if not FOIAbilityDoc.create(self):
			return False

		try:
			pdf_reader = PdfFileReader(open(self.obj['file_path'], 'rb'))
		except Exception as e:
			print "FOIAbilityPDF ERROR: could not load PDF from file_path"
			print e, type(e)
			return False

		try:
			# get number of pages
			self.obj['num_pages'] = pdf_reader.getNumPages()

			# keep tally of how many pages actually have text in them
			self.obj['num_pages_with_embedded_text'] = 0

			# for each page, attempt to extract text
			for page in xrange(self.obj['num_pages']):
				text, pdf_reader = extract_text_per_page(pdf_reader, page)
				
				# if page doesn't have text in it, move on
				if len(text) == 0:
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