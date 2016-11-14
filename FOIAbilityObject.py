import requests, json

class FOIAbilityObject():
	def __init__(self, id=None):
		self.obj = {
			"id" : id
		}

	def get_by_id(self):
		# inflate from solr by id

		if 'id' in self.obj.keys() and self.obj['id'] is not None:
			# query solr by id
			pass

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
		return True

	def save(self):
		# update self.obj to solr
		return True

	def delete(self):
		# remove itself from solr
		return True

	def emit(self, pretty=False):
		if pretty:
			print "**********\n"
			print json.dumps(self.obj, sort_keys=True, indent=4)
			print "\n**********\n"
		
		return json.dumps(self.obj)

