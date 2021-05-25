
import os
import nltk
import pytesseract
import re
import slate3k as slate
from pdf2image import convert_from_path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from PIL import Image
nltk.download("stopwords")
nltk.download("punkt")


def extractText(file):
    #pdfFileObj = open(pdfFileName, "rb")
    pdfFileObj = open(file, "rb")
    pdfPages = slate.PDF(pdfFileObj)

    # Extract text from PDF file
    text = ""
    for page in pdfPages:
        text += page
    return text


def extractOCR(file):
    pages = convert_from_path(file, 500)

    image_counter = 1
    for page in pages:
        filename = "page_" + str(image_counter) + ".jpg"
        page.save(filename, "JPEG")
        image_counter = image_counter + 1

    limit = image_counter-1
    text = ""
    for i in range(1, limit + 1):
        filename = "page_" + str(i) + ".jpg"
        page = str(((pytesseract.image_to_string(Image.open(filename)))))
        page = page.replace("-\n", "")
        text += page
        os.remove(filename)
    return text


# print("What is the name of the PDF?")
# fileName = input("(Without .pdf file extension)\n")
#pdfFileName = fileName + ".pdf"
# option = input("Direct text extraction or OCR extraction? (text / OCR)\n")

# if option == "text":
#     text = extractText(pdfFileName)
#     summarize(text)
# elif option == "OCR":
#     text = extractOCR(pdfFileName)
#     summarize(text)
# else:
#     print("Not a valid option!")