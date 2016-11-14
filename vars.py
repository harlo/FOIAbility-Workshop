import os

DATA_DIR = os.path.join(os.path.expanduser('~'), "stash")
BUFFER_MAX = 65536

MIME_TYPES = {
	"pdf" : {
		"aliases" : [
			r'PDF document,?.*'
		],
		"full_name" : "application/pdf"
	}
}