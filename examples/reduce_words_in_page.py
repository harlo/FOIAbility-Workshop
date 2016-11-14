import json, string, re
from email.utils import parseaddr

LANG = "english"

def reduce_words_in_page(page_text, stopwords_file, language=None):
	# set some rules about how to handle certain cases
	replace_punctuation = string.maketrans(string.punctuation, (' ' * len(string.punctuation)))
	replace_numbers = r'^\d+$'

	def readjust(bag_of_words):
		bag_of_words = [word.strip() for word in bag_of_words]

		for word in bag_of_words:
			word_split = word.split(" ")
			if len(word_split) == 1:
				continue
			
			bag_of_words.remove(word)
			bag_of_words = (bag_of_words + word_split)
				
		return [word for word in bag_of_words if len(word) > 0]

	def filter_out_email_addresses(bag_of_words):
		email_addresses = []

		for word in bag_of_words:
			potential_email = parseaddr(word)
			if '@' in potential_email[1]:
				bag_of_words.remove(word)
				email_addresses.append(potential_email[1])

		return email_addresses, bag_of_words

	# load the stopwords file for specified language
	# ref: Stanford University NLP project
	try:
		with open(stopwords_file, 'rb') as S:
			stopwords = json.loads(S.read())[LANG if language is None else language]
	except Exception as e:
		print "reduce_words_in_page ERROR: could not load stopwords"
		print e, type(e)
		return None

	# create a bag of words from supplied text WITHOUT reducing to unique words:
	bag_of_words = [str(word.lower()) for word in page_text.replace('\n', " ").split(" ")]

	# this will probably still contain some cruft. so...
	# filter out email addresses
	email_addresses, bag_of_words = filter_out_email_addresses(bag_of_words)

	# next, remove punctuation
	bag_of_words = readjust([word.translate(replace_punctuation) for word in bag_of_words])

	# now, remove any numbers
	bag_of_words = readjust([word for word in bag_of_words if re.match(replace_numbers, word) is None])

	return bag_of_words, email_addresses, stopwords