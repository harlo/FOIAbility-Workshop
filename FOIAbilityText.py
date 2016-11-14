from examples.map_NER_per_page import map_NER_per_page
from examples.find_word_frequencies_per_page import find_word_frequencies_per_page

from FOIAbilityObject import FOIAbilityObject

class FOIAbilityText(FOIAbilityObject):
	def __init__(self, text_stream=None, parent_id=None, id=None):
		FOIAbilityObject.__init__(self, id=id)

		self.obj.update({
			"parent_id" : parent_id,
			"text_stream" : " ".join(text_stream.encode('ascii', 'ignore').split('\n'))
		})

		if not self.get_by_id():
			print "FOIAbilityText WARN: possibly new text. Creating it..."

			if not self.create():
				print "FOIAbilityText ERROR: could not create this unknown text"

	def set_hash(self):
		from hashlib import sha256

		try:
			h = sha256()
			h.update(self.obj['text_stream'])
			self.obj['id'] = h.hexdigest()
			
			return self.save()
		
		except Exception as e:
			print "FOIAbilityText ERROR: could not create hash"
			print e, type(e)
		
		return False

	def create(self):
		if self.obj['text_stream'] is None:
			print "FOIAbilityText ERROR: NO TEXT STREAM!"
			return False

		if not FOIAbilityObject.create(self):
			return False

		# give itself an id
		if not self.set_hash():
			return False

		# if it has a parent to link, do so
		if 'parent_id' in self.obj.keys() and self.obj['parent_id'] is not None:
			if not self.link_doc(self.obj['parent_id']):
				print "FOIAbilityText ERROR: could not link parent id"
				return False

		self.emit(pretty=True)
		return self.map_NER()

	def map_NER(self):
		# do NER mapping
		try:
			entities = map_NER_per_page(self.obj['text_stream'])
			for entity_type in entities.keys():
				self.obj["entities_%s" % entity_type] = ",".join(entities[entity_type])

			return True
		except Exception as e:
			print "FOIAbilityText ERROR: failure getting entities from NER"
			print e, type(e)

		return False

	def map_word_frequencies(self):
		return False

