from documentcloud import DocumentCloud

def upload_pdf_to_documentcloud(pdf, credentials):
	try:
		dc_client = DocumentCloud(**credentials)
		return dc_client.documents.upload(pdf, secure=True, force_ocr=True)
	except Exception as e:
		print "upload_pdf_to_documentcloud ERROR"
		print e, type(e)

	return None