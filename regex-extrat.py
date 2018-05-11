# importing required modules
from PyPDF2 import PdfFileReader
import tensorflow as tf


SPIRIT, STELLAARD, SLIGRO, INVALID = 'SPIRIT', 'STELLAARD', 'SLIGRO', 'INVALID'
vendorList = [SPIRIT, STELLAARD, SLIGRO]
FILE_NAME_LIST = ["Right-Spirit", "bakkerij-stellaard", "Sligro-5039531715112"]
fileName = FILE_NAME_LIST[0]
filePath = "ePDF/" + fileName + ".pdf"

# creating a pdf file object
pdfFileObj = open(filePath, 'rb')

# creating a pdf reader object
pdfReader = PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(0)

# extracting text from page
# print(pageObj.extractText())

contents = pdfReader.getPage(0).extractText().split('\n')
# print ("content", contents)

if not (contents is None and not contents):
    print ("content line 3", contents[3])

print ("contents", contents)
# closing the pdf file object
pdfFileObj.close()
