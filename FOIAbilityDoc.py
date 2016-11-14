import os
from vars import MIME_TYPES, DATA_DIR

class FOIAbilityDoc():
	def __init__(self, file_path=None, id=None):
		self.obj = {
			"file_path" : file_path,
			"id" : id
		}

		if not self.get_by_id() and self.create():
			print "FOIAbilityDoc ERROR: could not create this unknown document"
			return

		self.inflate()

	def get_by_file_path(self):
		# inflate from solr by file_path
		
		if self.obj['file_path'] is not None:
			pass

		return False

	def get_by_id(self):
		# inflate from solr by id

		if self.obj['id'] is not None:
			pass

		return False

	def create_doc_dir(self):
		# create a data directory

		if 'id' not in self.obj.keys() or self.obj['id'] is None:
			print "FOIAbilityDoc ERROR: no id"
			return False

		doc_dir = os.path.join(DATA_DIR, self.obj['id'])

		try:
			os.mkdir(doc_dir)
		except Exception as e:
			print "FOIAbilityDoc ERROR: could not create doc_dir"

		return os.path.exists(doc_dir)

	def set_hash(self):
		# sha256 hash is its id

		if 'file_path' not in self.obj.keys() or self.obj['file_path'] is None:
			print "FOIAbilityDoc ERROR: no file_path"
			return False

		from hashlib import sha256
		from vars import BUFFER_MAX

		h = sha256()
		with open(self.obj['file_path'], 'rb') as f:
			d = f.read(BUFFER_MAX)
			while len(d) > 0:
				h.update(d)
				d = f.read(BUFFER_MAX)

		self.obj['id'] = h.hexdigest()
		return self.save()

	def set_mime_type(self):
		# find out what the mime type is and set to self.obj
		
		if 'file_path' not in self.obj.keys() or self.obj['file_path'] is None:
			print "FOIAbilityDoc ERROR: no file_path"
			return False

		import magic, re

		with magic.Magic() as m:
			mime_type = m.id_filename(self.obj['file_path'])

		print mime_type

		for m in MIME_TYPES.keys():
			for alias in MIME_TYPES[m]['aliases']:
				if re.match(alias, mime_type) is not None:
					self.obj['mime_type'] = MIME_TYPES[m]['full_name']
					break

			if "mime_type" in self.obj.keys():
				break

		return self.save()

	def link_doc(self, id):
		# add another doc as a reference
		return self.save()

	def add_data(self, key, value):
		# add data to be indexed in the doc
		return self.save()

	def inflate(self):
		# inflate all the data from flat files into object
		return False

	def create(self):
		return self.set_hash() and \
			self.set_mime_type() and \
			self.create_doc_dir()

	def save(self):
		# save self.obj to solr
		return True
