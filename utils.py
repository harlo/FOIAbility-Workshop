import os, json, requests

def setup_schema():
	schema_dir = os.path.join(os.getcwd(), "lib", "schema")
	schema_url = "http://localhost:8983/solr/FOIAbility/schema/fields"

	for _, _, s in os.walk(schema_dir):
		for schema in s:
			with open(os.path.join(schema_dir, schema), 'rb') as S:
				_= requests.post(schema_url, data=json.dumps({ "add-field" : json.loads(S.read()) }))

def get_credentials(key):
	return None