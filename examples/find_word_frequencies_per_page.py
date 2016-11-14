from examples.reduce_words_in_page import reduce_words_in_page

def find_word_frequencies_per_page(page_text, stopwords_file, language=None):
	bag_of_words, email_addresses, stopwords = reduce_words_in_page(page_text, stopwords_file, language=language)

	# first, filter out any stopwords
	bag_of_words = [word for word in bag_of_words if not word in stopwords]
	
	# add the email addresses back
	bag_of_words = (bag_of_words + email_addresses)

	#calculate frequencies
	word_frequencies = {}
	for word in bag_of_words:
		if word not in word_frequencies.keys():
			word_frequencies[word] = 0

		word_frequencies[word] += 1

	return word_frequencies
