import os, re

from examples.map_NER_per_page import map_NER_per_page
from examples.find_word_frequencies_per_page import find_word_frequencies_per_page
from examples.get_bag_of_words_per_page import get_bag_of_words_per_page
from examples.check_for_gibberish import check_for_gibberish
from vars import MISC_DIR

from FOIAbilityObject import FOIAbilityObject

STOPWORDS_PATH = os.path.join(MISC_DIR, "stopwords.json")

class FOIAbilityText(FOIAbilityObject):
	def __init__(self, text_stream=None, parent_id=None, id=None):
		FOIAbilityObject.__init__(self, id=id)

		self.obj.update({
			"parent_id" : parent_id
		})

		if text_stream is not None:
			self.obj.update({
				"text_stream" : " ".join(text_stream.encode('ascii', 'ignore').split('\n'))
			})

		if not self.get_by_id():
			#print "FOIAbilityText WARN: possibly new text. Creating it..."
			pass

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

		if check_for_gibberish(self.obj['text_stream']):
			print "FOIAbilityText ERROR: THIS TEXT IS GARBAGE!"
			return False

		# give itself an id
		if not self.set_hash():
			return False

		# if it has a parent to link, do so
		if 'parent_id' in self.obj.keys() and self.obj['parent_id'] is not None:
			if not self.link_doc(self.obj['parent_id']):
				print "FOIAbilityText ERROR: could not link parent id"
				return False

		if self.get_bag_of_words() and \
			self.map_NER() and \
			self.map_word_frequencies():

			return FOIAbilityObject.create(self)

	def map_NER(self):
		try:
			entities = map_NER_per_page(self.obj['text_stream'])

			if entities is not None:
				self.obj['entities'] = entities

			return True
		except Exception as e:
			print "FOIAbilityText ERROR: failure getting entities from NER"
			print e, type(e)

		return False

	def inflate_entities(self):
		entities = {}
		for key in self.obj.keys():
			entity = re.findall(r'entities\.(.*)', key)

			if len(entity) == 0:
				continue

			try:
				entities[entity[0]] = self.obj[key]
				del self.obj[key]

			except Exception as e:
				print e, type(e)
				continue

		self.obj['entities'] = entities

	def map_word_frequencies(self):
		try:
			self.obj['word_frequencies'] = find_word_frequencies_per_page(self.obj['text_stream'], STOPWORDS_PATH)
			
			return True
		except Exception as e:
			print "FOIAbilityText ERROR: failure mapping word frequencies"
			print e, type(e)

		return False

	def inflate_word_frequencies(self):
		word_frequencies = {}
		for key in self.obj.keys():
			word_frequency = re.findall(r'word_frequencies\.(.*)', key)			
			
			if len(word_frequency) == 0:
				continue

			try:
				word_frequencies[word_frequency[0]] = self.obj[key][0]
				del self.obj[key]
				
			except Exception as e:
				print e, type(e)
				continue

		self.obj['word_frequencies'] = word_frequencies

	def get_bag_of_words(self):
		try:
			self.obj['bag_of_words'] = get_bag_of_words_per_page(self.obj['text_stream'], STOPWORDS_PATH)
			
			return True
		except Exception as e:
			print "FOIAbilityText ERROR: failure getting bag of words"
			print e, type(e)

		return False

	def inflate(self, data, extra_omits=None):
		# solr borks nesting!

		if not FOIAbilityObject.inflate(self, data, extra_omits=extra_omits):
			return False
		
		self.inflate_word_frequencies()
		self.inflate_entities()
		return True

