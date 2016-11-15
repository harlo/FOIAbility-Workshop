import os
from sys import argv, exit
from fabric.api import settings, local

from FOIAbilityPDF import FOIAbilityPDF

def batch_index(batch_dir):
	for r, _, files in os.walk(batch_dir):
		for f in files:

			with settings(warn_only=True):
				local("python FOIAbility.py --i %s" % os.path.join(r, f))

		break

def index(file_path):
	pdf = FOIAbilityPDF(file_path)
	pdf.emit(pretty=True)

if __name__ == "__main__":
	if len(argv) == 3:
		
		if argv[1] in ["index", "--i"] and os.path.exists(argv[2]):
			index(argv[2])

		if argv[1] in ["batch", "--b"] and os.path.isdir(argv[2]):
			batch_index(argv[2])
