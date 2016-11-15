import os, json, requests
from vars import SOLR_URL, SOLR_HEADER, SOLR_DYNAMIC_FIELDS, CONF_DIR

def setup_schema():
	schema_dir = os.path.join(os.getcwd(), "lib", "schema")

	for _, _, s in os.walk(schema_dir):
		for schema in s:
			with open(os.path.join(schema_dir, schema), 'rb') as S:

				if s in ["%s.json" % d for d in SOLR_DYNAMIC_FIELDS]:
					print "INSERTING A DYNAMIC FIELD!"
					field_type = "add-dynamic-field"
				else:	
					field_type = "add-field"

				_= requests.post("%s/schema/fields" % SOLR_URL, \
					data=json.dumps({ "%s" % field_type : json.loads(S.read()) }), \
					headers=SOLR_HEADER)

def get_credentials(key):
	try:
		with open(os.path.join(CONF_DIR, "secrets.json"), 'rb') as C:
			config = json.loads(C.read())
	except Exception as e:
		print "get_credentials ERROR: could not load secrets from file"
		print e, type(e)
		return None

	try:
		return config[key]
	except Exception as e:
		print "get_credentials ERROR: key %s not found in secrets config" % key
		print e, type(e)

	return None