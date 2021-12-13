from flask import Flask, redirect, url_for, request ,render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
import webbrowser
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    return render_template('hello.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        a=request.form['no']
        a = int(a)-1 
        b=int(request.form['angle'])
        
        f = request.files['file']
        f.save(secure_filename(f.filename))
        pdf_path = (
                Path.home()
                / 'Downloads'
                / 'flask_pdf_rotation'
                / f.filename
            )
        pdf_reader = PdfFileReader(str(pdf_path))
        # a=1
        # b=90
        # pdf_reader = PdfFileReader(str(request.files['file']))
        pdf_writer = PdfFileWriter()
        for n in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(n)
            if n==a:
                page.rotateClockwise(b)
            pdf_writer.addPage(page)
        with Path("rotated.pdf").open(mode="wb") as output_file:
            pdf_writer.write(output_file)
        pdf_reader = PdfFileReader(str(pdf_path))

        return send_from_directory(os.path.abspath(os.getcwd()), 'rotated.pdf')

if __name__ == '__main__':
   app.run()