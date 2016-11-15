import re
from PyPDF2 import PdfFileReader

from FOIAbilityDoc import FOIAbilityDoc
from FOIAbilityText import FOIAbilityText
from examples.extract_text_per_page import extract_text_per_page
from examples.download_ocr_text_per_page import download_ocr_text_per_page
from examples.parse_metadata_from_pdf import parse_metadata_from_pdf

from utils import get_credentials
from vars import MIME_TYPES

MODES = MIME_TYPES['pdf']['eval_modes']

class FOIAbilityPDF(FOIAbilityDoc):
	def __init__(self, file_path=None, id=None):
		FOIAbilityDoc.__init__(self, file_path=file_path, id=id)

	def create(self):
		try:
			self.pdf_reader = PdfFileReader(open(self.obj['file_path'], 'rb'))
		except Exception as e:
			print "FOIAbilityPDF ERROR: could not load PDF from file_path"
			print e, type(e)
			return False

		if self.evaluate_text() and \
			self.evaluate_metadata():

			return FOIAbilityDoc.create(self)

		return False

	def evaluate_metadata(self):
		try:
			metadata = parse_metadata_from_pdf(self.obj['file_path'])
			if metadata is not None:
				self.obj['metadata'] = metadata

			return True
		except Exception as e:
			print "FOIAbilityPDF ERROR: could not get metadata from pdf"
			print e, type(e)

		return False

	def inflate_metadata(self):
		# solr borks nested values
		metadata = {}
		for key in self.obj.keys():
			m = re.findall(r'metadata\.(.*)', key)

			if len(m) == 0:
				continue

			try:
				metadata[m[0]] = self.obj[key]
				del self.obj[key]

			except Exception as e:
				print e, type(e)
				continue

		self.obj['metadata'] = metadata

	def evaluate_text(self, mode=MODES['PyPDF']):
		try:
			# get number of pages
			self.obj['num_pages'] = self.pdf_reader.getNumPages()

			# keep tally of how many pages actually have text in them
			self.obj['num_pages_with_embedded_text'] = 0

			# for each page, attempt to extract text
			for page in xrange(self.obj['num_pages']):
				print "FOIAbilityPDF INFO: Indexing page %d/%d" % (page + 1, self.obj['num_pages'])
				
				# UNCOMMENT FOR TESTING
				'''
				if page > 5:
					break
				'''

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
						text = download_ocr_text_per_page(page, get_credentials('Documentcloud'))
					except Exception as e:
						print "FOIAbilityPDF WARN: could not get text from page (mode Documentcloud)"
						print e, type(e)
						continue
				
				# if page doesn't have text in it, move on
				if text is None or len(text) == 0:
					continue

				# make indexible text object for text
				try:
					self.link_doc(FOIAbilityText(text_stream=text, parent_id=self.obj['id']).obj['id'])
				except Exception as e:
					print "FOIAbilityPDF WARN: could not link text object to parent"
					print e, type(e)
					continue

				# increment tally on success
				self.obj['num_pages_with_embedded_text'] = (self.obj['num_pages_with_embedded_text'] + 1)

			return True
		except Exception as e:
			print "FOIAbilityPDF ERROR: could not get number of pages in this PDF"
			print e, type(e)
		
		return False

	def inflate(self, data, extra_omits=None):
		if not FOIAbilityDoc.inflate(self, data, extra_omits=extra_omits):
			return False

		self.inflate_metadata()
		return True