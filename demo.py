from sys import argv

from FOIAbilityPDF import FOIAbilityPDF

def create_pdf_object(file_path):
	pdf = FOIAbilityPDF(file_path=file_path)
	pdf.emit(pretty=True)

if __name__ == "__main__":
	create_pdf_object(argv[1])