import ner

def map_NER_per_page(page_text, NER_port=2020):
	'''
		Uses Stanford's NER to create a map of entities contained in the text.

		arguments:
			page_text: (string) the page's full text
			NER_port: (int) port the NER server runs on. defaults to 2020
	'''

	NER_socket = ner.SocketNER(host="localhost", port=NER_port)

	try:
		result = NER_socket.get_entities(page_text)
		entities = {}
		
		for entity_type in [str(key) for key in result.keys()]:
			entities[entity_type] = list(set([str(entity) for entity in result[entity_type]]))

		return entities
	except Exception as e:
		print "map_NER_per_page ERROR"
		print e, type(e)

	return None