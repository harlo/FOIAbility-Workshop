import json, re, os
from sys import argv
from time import sleep
from fabric.api import settings, local

from FOIAbilityPDF import FOIAbilityPDF
from FOIAbilityText import FOIAbilityText

def setup(file_path):
	pdf = FOIAbilityPDF(file_path=file_path)
	pdf.emit(pretty=True)
	
	return pdf

def step_through_keywords(file_path):
	pdf = setup(file_path)
	pdf.emit(pretty=True)

	current_page = 0

	while True:
		try:
			if raw_input("PRESS ENTER TO SEE KEYWORDS ON THIS PAGE") == '':
				text = FOIAbilityText(id=pdf.obj['linked_docs'][current_page])
				
				print "********* BAG OF WORDS *********\n"
				print [str(w) for w in text.obj['bag_of_words']]
				print "\n********* NAMED ENTITIES *********\n"
				print json.dumps(text.obj['entities'], indent=4)
				
				current_page += 1
		
		except KeyboardInterrupt as e:
			break
		except IndexError as e:
			print "NO MORE PAGES INDEXED IN DOCUMENT %s" % pdf.obj['file_path']
			break

def search_by_keywords(file_path):
	pdf = setup(file_path)
	res = pdf.search_by_keywords(["kelly", "scott"])

	page = 0

	while True:
		try:
			if raw_input("PRESS ENTER TO CYCLE THROUGH RESULTS") == '':
				#text = FOIAbilityText(id=res[page]['id'])
				
				print "********* KEYWORD INFO *********\n"
				print "Found in page %d of document" % (pdf.obj['linked_docs'].index(res[page]['id']) + 1)
				for key in res[page].keys():
					word = re.findall(r'word_frequencies\.(.*)', key)
					if len(word) == 0:
						continue

					print "[%s] %d mentions" % (word[0].upper(), res[page][key][0])

				page += 1
				print "\n**************************\n\n"
		except KeyboardInterrupt as e:
			break
		except IndexError as e:
			print "NO MORE RESULTS IN DOCUMENT %s" % pdf.obj['file_path']
			break

def batch_index():
	for r, _, files in os.walk("/home/harlo/stash"):
		for f in files:

			with settings(warn_only=True):
				local("python FOIAbility.py --i %s" % os.path.join(r, f))

		break

if __name__ == "__main__":
	batch_index()