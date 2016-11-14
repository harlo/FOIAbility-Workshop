from fabric.api import settings, local
from bs4 import BeautifulSoup

from vars import LIB_DIR, MISC_DIR, MIME_TYPES

def parse_metadata_from_pdf(pdf):
	# use Peepdf to locate metadata
	with settings(warn_only=True):
		raw_metadata = local("%s/Peepdf/peepdf.py %s -s %s/peepdf_batch.txt" % (LIB_DIR, pdf, MISC_DIR), capture=True)

	if raw_metadata.return_code is not 1:
		print "parse_metadata_from_pdf ERROR: no raw metadata returned from Peepdf"
		return None

	# pull out each XML block for analysis
	metadata = {}
	METADATA_MAP = MIME_TYPES['pdf']['metadata']
	FACET_INDICES = [m['label'] for m in MIME_TYPES['pdf']['metadata']]

	for line in raw_metadata.splitlines():
		tag = BeautifulSoup(line.strip(), "html.parser")
		
		if bool(tag.find()) and tag.string is not None:
			tag_name = str(tag.children.next().name)
			
			# preserve the important fields
			if tag_name in FACET_INDICES:
				facet = METADATA_MAP[FACET_INDICES.index(tag_name)]
				alias = facet['alias']
				
				if 'is_bag' in facet.keys() and facet['is_bag']:
					if alias not in metadata.keys():
						metadata[alias] = []
					
					metadata[alias].append(str(tag.string))
				
				else:
					metadata[alias] = str(tag.string)

	return metadata if len(metadata.keys()) > 0 else None
