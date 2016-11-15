import requests, json
from copy import deepcopy

from vars import SOLR_URL, SOLR_HEADER, RESPONSE_OMIT, PRETTY_OMIT_FIELDS

class FOIAbilityObject():
	def __init__(self, id=None):
		self.obj = {
			"id" : id
		}

	def query_by_facet(self, facet, constraint):
		url = "%s/select?q=%s:%s&wt=json" % (SOLR_URL, facet, constraint)

		try:
			r = requests.get(url, headers=SOLR_HEADER)
			if r.status_code != 200:
				print "FOIAbilityObject ERROR: bad response"
				return None

			return r.json()['response']['docs']
		except Exception as e:
			print "FOIAbilityObject ERROR: bad response"
			print e, type(e)

		return None

	def get_by_id(self):
		# inflate from solr by id

		if 'id' not in self.obj.keys() or self.obj['id'] is None:
			return False
		
		try:
			# query solr by id
			r = self.query_by_facet("id", self.obj['id'])[0]

			if r is None or r['id'] != self.obj['id']:
				print "FOIAbilityObject ERROR: couldn't find id %s" % self.obj['id']
				return False

			return self.inflate(r)
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

	def inflate(self, data, extra_omits=None):
		for omit in RESPONSE_OMIT['inflate']:
			del data[omit]

		if extra_omits is not None:
			for omit in extra_omits:
				del data[omit]

		self.obj.update(data)
		return True

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
				"FOIAbilityObject SUCCESS: doc %s created" % self.obj['id']
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
				"FOIAbilityObject SUCCESS: doc %s deleted" % self.obj['id']
				return True

		except Exception as e:
			print "FOIAbilityObject ERROR: couldn't delete doc %s" % self.obj['id']
			print e, type(e)

		return False

	def emit(self, pretty=False):
		if pretty:
			pretty_emit = deepcopy(self.obj)
			pretty_omit = []

			for key in pretty_emit.keys():
				if key in PRETTY_OMIT_FIELDS:
					del pretty_emit[key]
					pretty_omit.append(str(key))

			print "**********\n"
			print json.dumps(pretty_emit, sort_keys=True, indent=4)
			print "\nplus fields not shown here: %s" % pretty_omit
			print "\n**********\n"
		
		return self.obj

