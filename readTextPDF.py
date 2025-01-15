import pymupdf

# Create a PDF reader object
def getTextPDF(pdfFile, page)
    doc = pymupdf.open(pdfFile)
    for i in range(10):
        text = doc.load_page(i).get_text("text")
        for line in text:
            print(line)
