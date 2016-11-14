import os

DATA_DIR = os.path.join(os.path.expanduser('~'), "stash")
LIB_DIR = os.path.join(os.getcwd(), "lib")
MISC_DIR = os.path.join(LIB_DIR, "misc")

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
		}
	}
}