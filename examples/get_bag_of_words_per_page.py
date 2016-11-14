from examples.reduce_words_in_page import reduce_words_in_page

def get_bag_of_words_per_page(page_text, stopwords_file, language=None):	
	bag_of_words, email_addresses, stopwords = reduce_words_in_page(page_text, stopwords_file, language=language)

	# filter out any stopwords
	bag_of_words = list(set(bag_of_words) - set(stopwords))
	
	# add email addresses back
	return list(set((bag_of_words + email_addresses)))