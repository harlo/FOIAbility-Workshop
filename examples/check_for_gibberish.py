import nltk
from fractions import Fraction

from vars import SIGNIFIGANT_PARTS_OF_SPEECH, PUNCTUATION, PUNCTUATION_THRESHOLD_MIN, PUNCTUATION_THRESHOLD_MAX, SIGNIFICANT_THRESHOLD_MAX, WORD_LENGTH_THRESHOLD

def check_for_gibberish(text):
	try:
		text = nltk.word_tokenize(text)
		parts_of_speech = nltk.pos_tag(text)

		# with parts of speech identified, ask 2 questions:
		# what are the ratios of signifigant words and punctuation to overall number of words?
		# what's the mean word length?		

		num_signifigant_words = 0
		num_punctuation = 0
		word_lengths = []

		for pos in parts_of_speech:
			word_lengths.append(len(pos[0]))

			try:
				if str(pos[0]) in PUNCTUATION:
					num_punctuation += 1
					continue
			
			except UnicodeEncodeError as e:
				continue

			if str(pos[1]) in PUNCTUATION:
				num_punctuation += 1
				continue

			if str(pos[1]) in SIGNIFIGANT_PARTS_OF_SPEECH:
				num_signifigant_words += 1
				#print pos
				continue
			
			#print pos

		try:
			AVERAGE_WORD_LENGTH = (sum(word_lengths) / len(word_lengths))
		except ZeroDivisionError as e:
			print "check_for_gibberish WARN: Dividing average word length by zero :("
			AVERAGE_WORD_LENGTH = 0


		print "\n\n*************"
		print "AVERAGE LENGTHS: %f" % AVERAGE_WORD_LENGTH
		print "SIGNIFICANT-WORDS-TO-PUNCTUATION (total %d): %d / %d" % (len(word_lengths), num_signifigant_words, num_punctuation)

		def ratio(a, b):
			a = float(a)
			b = float(b)

			if b == 0:
				return a
			
			return ratio(b, a % b)

		try:
			w = ratio(num_signifigant_words, len(word_lengths))
			ratio_significant_words = float((num_signifigant_words/w) / (len(word_lengths)/w))
		except ZeroDivisionError as e:
			print "check_for_gibberish WARN: Dividing sig ratio by zero :("
			ratio_significant_words = 0

		try:
			p = ratio(num_punctuation, len(word_lengths))
			ratio_punctuation = float((num_punctuation/p) / (len(word_lengths)/p))
		except ZeroDivisionError as e:
			print "check_for_gibberish WARN: Dividing punctuation ratio by zero :("
			ratio_punctuation = 0

		# deliberate.
		# DISCLAIMER: i threw this together quickly, so
		# let's discuss! could be wrong!
		
		print "RATIO OF SIGNIFICANT WORDS TO ALL WORDS: %f" % ratio_significant_words
		print "RATIO OF PUNCTUATION TO ALL WORDS: %f" % ratio_punctuation
		print "*************\n\n"

		if AVERAGE_WORD_LENGTH == 0:
			return True

		if ratio_punctuation >= PUNCTUATION_THRESHOLD_MAX:
			return True

		if ratio_significant_words >= SIGNIFICANT_THRESHOLD_MAX:
			return False

		if (ratio_punctuation > PUNCTUATION_THRESHOLD_MIN) and (AVERAGE_WORD_LENGTH < WORD_LENGTH_THRESHOLD):
			return True

		return False

	except Exception as e:
		print "check_for_gibberish ERROR: cannot check this text"
		print e, type(e)

	return True