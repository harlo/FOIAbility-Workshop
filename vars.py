import os, string

DATA_DIR = os.path.join(os.path.expanduser('~'), "stash")
LIB_DIR = os.path.join(os.getcwd(), "lib")
MISC_DIR = os.path.join(LIB_DIR, "misc")

SOLR_URL = "http://localhost:8983/solr/FOIAbility"
SOLR_HEADER = {"Content-Type" : "application/json"}

BUFFER_MAX = 65536

MIME_TYPES = {
	"pdf" : {
		"aliases" : [
			r'PDF document,?.*'
		],
		"full_name" : "application/pdf",
		"eval_modes" : {
			"PyPDF" : 1,
			"Documentcloud" : 2
		},
		"metadata" : [
			{
				"label" : "rdf:li",
				"alias" : "bag_element",
				"is_bag" : True
			},
			{
				"label" : "pdfx:company",
				"alias" : "company"
			},
			{
				"label" : "pdfx:_authoremail",
				"alias" : "author_email"
			},
			{
				"label" : "pdfx:_authoremaildisplayname",
				"alias" : "author_display_name"
			},
			{
				"label" : "xmp:creatortool",
				"alias" : "creator_tool"
			},
			{
				"label" : "pdf:producer",
				"alias" : "producer"
			},
			{
				"label" : "xmp:modifydate",
				"alias" : "modify_date"
			},
			{
				"label" : "xmp:createdate",
				"alias" : "create_date"
			},
			{
				"label" : "xmp:metadatadate",
				"alias" : "metadata_date"
			}
		]
	}
}

PUNCTUATION = list(string.punctuation) + ['``', '\'\'']
PUNCTUATION_THRESHOLD_MAX = 0.65
PUNCTUATION_THRESHOLD_MIN = 0.28

SIGNIFIGANT_PARTS_OF_SPEECH = [
	'VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB',
	'RBS', 'RBR', 'RB', 'WDT',
	'PRP$', 'PRP', 'PDT',
	'MD', 'IN', 'EX',
	'JJS', 'JJR', 'JJ',
	'DT', 'CC'
]
SIGNIFICANT_THRESHOLD_MAX = 1.0
SIGNIFICANT_THRESHOLD_MIN = 0.31

WORD_LENGTH_THRESHOLD = 1.0