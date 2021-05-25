from urllib.request import urlopen
from flask import Flask, app,render_template,request
import os
from bert import bert
from bs4 import BeautifulSoup
from sumy_sum import sumy_summarization
from sq2sq import sq2sq
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PyPDF2 import PdfFileReader,PdfFileWriter
# from pandas.compat import StringIO

app = Flask(__name__, static_url_path="", static_folder="static")

#app.config['UPLOAD_FOLDER']= 'C:/Users/abhim/Documents/Python/sum_new/static/'

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) +'/uploads/'
# DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) 
# app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def fun():
    summary=''
    if request.method=='POST':
        word = request.form['word']
        word=int(word)
        text = request.form['text']
        summary=bert(text,word)
        print(summary)
        return render_template('index.html',summary=summary)    
    else:
        return render_template('index.html')


@app.route('/link', methods=['GET', 'POST'])
def link():
    summary=''
    if request.method=='POST':
        url = request.form['link']
        word=request.form['word']
        word=int(word)
        page = urlopen(url)
        soup = BeautifulSoup(page)
        fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
        #max_value = sent_tokenize(fetched_text)
        summary = bert(fetched_text, word)
    return render_template('link.html',summary=summary)


@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
    summary=''
    if request.method=='POST':
        word = request.form['word']
        word=int(word)
        #file_pdf = request.files['file']
        f = request.files['file']
        filename=secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER,filename))
        pdffileobj=open(os.path.join(UPLOAD_FOLDER,filename),'rb')
        pdfreader=PdfFileReader(pdffileobj)
        x=pdfreader.numPages
        text=''
        count=0
        while (count < 5 and count < x):
            pageobj=pdfreader.getPage(count)
            text= text + pageobj.extractText()
            count+=1
            print(text,count)
        pdffileobj.close()
        print(text)

        #print(type(file_pdf))
        #print(file_pdf.read())
        # rsrcmgr = PDFResourceManager()
        # sio = StringIO()
        # codec = 'utf-8'
        # laparams = LAParams()
        # device = TextConverter(rsrcmgr, sio, laparams=laparams)
        # interpreter = PDFPageInterpreter(rsrcmgr, device)

        # # Extract text
        # fp = open("C:/Users/abhim/Documents/Python/sum_new/static/"+ f.filename, 'rb') 
        # for page in PDFPage.get_pages(fp):
        #     interpreter.process_page(page)
        # fp.close()

        # # Get text from StringIO
        # text = sio.getvalue()
        summary=bert(text,word)
        print(summary)
    return render_template('pdf.html',summary=summary)    
    


@app.route('/compare', methods=['GET', 'POST'])
def fu3():
    summary=''
    sumy_summary=''
    spacy_summary=''
    if request.method=='POST':
        word = request.form['word']
        word=int(word)
        text = request.form['text']
        summary=bert(text,word)
        spacy_summary=sq2sq(text,word)
        sumy_summary=sumy_summarization(text,word)
        print(summary)
    return render_template('compare.html',summary=summary,sumy_summary=sumy_summary,spacy_summary=spacy_summary)    
    


port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    app.run(debug=True, port=port)