from documentcloud import DocumentCloud
from time import sleep

DC_PRIVATE = "private"
DC_PUBLIC = "public"
DC_PENDING = "pending"
WORKAROUND_SLEEP = 5

def download_ocr_text_per_page(documentcloud_id, page_num, credentials):
	page_text = None
	
	try:
		dc_client = DocumentCloud(**credentials)
		obj = dc_client.documents.get(documentcloud_id)

		'''
		workaround for private docs is, set public, wait, then private again.
		https://github.com/documentcloud/documentcloud/issues/220
		'''
		
		apply_access_workaround = (obj.access == DC_PRIVATE)
		
		if apply_access_workaround:
			obj.access = DC_PUBLIC
			obj.put()

			while obj.access in [DC_PRIVATE, DC_PENDING]:
				sleep(WORKAROUND_SLEEP)
				obj = dc_client.documets.get(documentcloud_id)

		page_text = obj.get_page_text(page_num)

		if apply_access_workaround:
			obj.access = DC_PRIVATE
			obj.put()

	except Exception as e:
		print "download_ocr_text_per_page ERROR"
		print e, type(e)

	return page_text