import PyPDF2

pdf = PyPDF2.PdfFileReader("./res/document.pdf")
info = pdf.getDocumentInfo()

for i in info:
    print(info[i])