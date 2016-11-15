import requests, json
import xml.etree.ElementTree as et
from xmljson import parker


from vars import SOLR_URL, SOLR_HEADER

class FOIAbilityObject():
	def __init__(self, id=None):
		self.obj = {
			"id" : id
		}

	def __parse_xml_response(self, xml):
		return json.loads(json.dumps(parker.data(et.fromstring(xml))))

	def query_by_facet(self, facet, constraint):
		print "\n\n*************"
		print "GETTING BY FACET!"
		print "*************\n\n"
		
		url = "%s/select?q=%s:%s" % (SOLR_URL, facet, constraint)

		try:
			r = requests.get(url, headers=SOLR_HEADER)
			if r.status_code != 200:
				print "FOIAbilityObject ERROR: bad response"
				print r.text
				return None

			return self.__parse_xml_response(r.text)['result']['doc']
		except Exception as e:
			print "FOIAbilityObject ERROR: bad response"
			print e, type(e)

		return None

	def get_by_id(self):
		# inflate from solr by id

		if 'id' not in self.obj.keys() or self.obj['id'] is None:
			return False

		# query solr by id
		r = self.query_by_facet("id", self.obj['id'])
		
		try:
			if r is None or r['str'] != self.obj['id']:
				print "FOIAbilityObject ERROR: couldn't find id %s" % self.obj['id']
				return False

			return True
		except Exception as e:
			print "FOIAbilityObject ERROR: couldn't find id %s" % self.obj['id']
			print e, type(e)

		return False

	def link_doc(self, doc_id):
		# add another doc as a reference
		if doc_id is None:
			print "FOIAbilityObject ERROR: cannot link doc because doc_id is None"
			return False

		if 'linked_docs' not in self.obj.keys():
			self.obj['linked_docs'] = []
		
		self.obj['linked_docs'].append(doc_id)
		return self.save()

	def add_data(self, key, value):
		# add data to be indexed in the doc
		return False

	def create(self):
		# create in solr
		try:		
			r = requests.post("%s/update/json/docs?commit=true" % SOLR_URL, \
				data=json.dumps(self.emit()), headers=SOLR_HEADER)

			if r.status_code != 200:
				print "FOIAbilityObject ERROR: couldn't create doc %s" % self.obj['id']
				print r.text
				return False

			if r.json()['responseHeader']['status'] == 0:
				return True

		except Exception as e:
			print "FOIAbilityObject ERROR: couldn't create doc %s" % self.obj['id']
			print e, type(e)

		return False

	def save(self):
		# update self.obj to solr
		return True

	def delete(self):
		# remove itself from solr		
		try:
			r = requests.post("%s/update?commit=true" % SOLR_URL, \
				data=json.dumps({"delete" : {"id" : self.obj['id']}}), headers=SOLR_HEADER)

			if r.status_code != 200:
				print "FOIAbilityObject ERROR: couldn't delete doc %s" % self.obj['id']
				print r.text
				return False

			if r.json()['responseHeader']['status'] == 0:
				return True

		except Exception as e:
			print "FOIAbilityObject ERROR: couldn't delete doc %s" % self.obj['id']
			print e, type(e)

		return False

	def emit(self, pretty=False):
		if pretty:
			print "**********\n"
			print json.dumps(self.obj, sort_keys=True, indent=4)
			print "\n**********\n"
		
		return self.obj

