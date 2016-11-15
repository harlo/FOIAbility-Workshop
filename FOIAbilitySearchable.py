import requests, json
from vars import SOLR_URL, SOLR_HEADER

class FOIAbilitySearchable():
	def __init__(self):
		pass

	def __build_query(self, query, fields=None, all_fields=False, pretty=True):
		query = "q=%s&wt=json" % (query)

		if not all_fields:
			if fields is not None and type(fields) is list:
				if "id" not in fields:
					fields.append("id")

				fields = ",".join(fields)
			else:
				fields = "id"

			query = "%s&fl=%s" % (query, fields)

		return self.general_query(query, pretty=pretty)

	def general_query(self, query, pretty=True):
		url = "%s/select?%s&wt=json" % (SOLR_URL, query)

		try:
			r = requests.get(url, headers=SOLR_HEADER)
			if r.status_code != 200:
				print "FOIAbilitySearchable ERROR: bad response"
				return None

			result = r.json()['response']['docs']
			
			if pretty:
				print "\n**********\n"
				print "FOIAbilitySearchable RESULT: query succeeded"
				print "query: %s" % url
				print "num results: %d" % len(result)
				print "\n**********\n"
				print "\n**********\n"
				print json.dumps(result, sort_keys=True, indent=4)
				print "\n**********\n"
			
			return result
		except Exception as e:
			print "FOIAbilitySearchable ERROR: bad response"
			print e, type(e)

		return None

	def get_all_with_same_mime_type(self):
		# returns all documents that share the same mime type
		return self.__build_query("mime_type:%s" % self.obj['mime_type'], fields=["file_path"])

	def search_by_keywords(self, keywords):
		if type(keywords) in [str, unicode]:
			keywords = [keywords]

		if type(keywords) is not list:
			print "FOIAbilitySearchable ERROR: keywords must be list"
			return None

		print "FOIAbilitySearchable INFO: searching within document %s for %s" % (self.obj['file_path'], keywords)

		# constrain search to items in linked docs
		if 'linked_docs' not in self.obj.keys():
			print "FOIAbilitySearchable ERROR: no linked documents to search within"
			return None

		# let's add some extra fields for analysis, too!
		# word frequencies, and anything else
		extra_fields = ["word_frequencies.%s" % k for k in keywords]

		if len(keywords) > 1:
			keywords = "(%s)" % " AND ".join(keywords)
		else:
			keywords = keywords[0]

		query = "bag_of_words:%s&fq=id:(%s)" % (keywords, " ".join(self.obj['linked_docs']))
		return self.__build_query(query, fields=extra_fields)
		