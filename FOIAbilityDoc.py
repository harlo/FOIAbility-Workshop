import os
from vars import MIME_TYPES, DATA_DIR

from FOIAbilityObject import FOIAbilityObject
from FOIAbilitySearchable import FOIAbilitySearchable

class FOIAbilityDoc(FOIAbilityObject, FOIAbilitySearchable):
	def __init__(self, file_path=None, id=None):
		FOIAbilityObject.__init__(self, id=id)

		self.obj.update({
			"file_path" : file_path
		})

		if not self.get_by_id() and not self.get_by_file_path():
			print "FOIAbilityDoc WARN: possibly new doc. Creating it..."

			if not self.create():
				print "FOIAbilityDoc ERROR: could not create this unknown document"

	def get_by_file_path(self):		
		if 'file_path' not in self.obj.keys() or self.obj['file_path'] is None:
			print "FOIAbilityDoc ERROR: no file_path"
			return False
				
		try:
			# query solr by file_path
			r = self.query_by_facet("file_path", self.obj['file_path'])[0]

			if r is None or r['file_path'] != self.obj['file_path']:
				print "FOIAbilityDoc ERROR: couldn't find any doc with at %s" % self.obj['file_path']
				return False

			return self.inflate(r)
		except Exception as e:
			print "FOIAbilityDoc ERROR: couldn't find any doc at %s" % self.obj['file_path']
			print e, type(e)

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
			print "FOIAbilityDoc WARN: could not create doc_dir (exists? %s)" % os.path.exists(doc_dir)
			print e, type(e)

		return os.path.exists(doc_dir)

	def set_hash(self):
		# sha256 hash is its id

		if 'file_path' not in self.obj.keys() or self.obj['file_path'] is None:
			print "FOIAbilityDoc ERROR: no file_path"
			return False

		from hashlib import sha256
		from vars import BUFFER_MAX

		try:
			h = sha256()
			with open(self.obj['file_path'], 'rb') as f:
				d = f.read(BUFFER_MAX)
				while len(d) > 0:
					h.update(d)
					d = f.read(BUFFER_MAX)

			self.obj['id'] = h.hexdigest()
			return True
		
		except Exception as e:
			print "FOIAbilityDoc ERROR: could not create hash"
		
		return False

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
				return True

		return False

	def inflate(self, data):
		# inflate all the data from Solr into object
		if FOIAbilityObject.inflate(self, data):
			FOIAbilitySearchable.__init__(self)

	def create(self):
		try:
			if self.set_hash() and \
				self.set_mime_type() and \
				self.create_doc_dir():

				return FOIAbilityObject.create(self)

		except Exception as e:
			print "FOIAbilityDoc ERROR: could not create document."
			print e, type(e)

		return False

	def delete(self, delete_file=False):
		try:
			if self.delete_doc_dir(delete_file=delete_file) and \
				self.unlink_docs():

				return FOIAbilityObject.delete(self)
		except Exception as e:
			print "FOIAbilityDoc ERROR: could not delete doc %s" % self.obj['id']
			print e, type(e)

		return False

	def unlink_docs(self):
		for doc_id in self.obj['linked_docs']:
			doc = FOIAbilityObject(id=doc_id)
			print doc.obj['id']

			try:
				doc.delete()
			except Exception as e:
				print "FOIAbilityDoc ERROR: couldn't delete linked doc %s" % doc_id
				print e, type(e)

		return True

	def delete_doc_dir(self, delete_file=False):
		# remove assets
		if 'id' not in self.obj.keys() or self.obj['id'] is None:
			print "FOIAbilityDoc ERROR: no id"
			return False

		from shutil import rmtree
		doc_dir = os.path.join(DATA_DIR, self.obj['id'])

		try:
			rmtree(doc_dir)
		except Exception as e:
			print "FOIAbilityDoc ERROR: could not remove doc_dir"
			return False

		if delete_file:
			try:
				os.remove(self.obj['file_path'])
			except Exception as e:
				print "FOIAbilityDoc WARN: could not remove original file from file_path"
				print e, type(e)

		return not os.path.exists(doc_dir)
