import os, json, requests
from vars import SOLR_URL, SOLR_HEADER

def setup_schema():
	schema_dir = os.path.join(os.getcwd(), "lib", "schema")

	for _, _, s in os.walk(schema_dir):
		for schema in s:
			with open(os.path.join(schema_dir, schema), 'rb') as S:
				_= requests.post("%s/schema/fields" % SOLR_URL, \
					data=json.dumps({ "add-field" : json.loads(S.read()) }), \
					header=SOLR_HEADER)

def get_credentials(key):
	return None