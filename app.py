import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask.json import jsonify
from flask import request
from flask_api import status
from werkzeug.utils import secure_filename
import text_helper

app = Flask(__name__)

UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/ocr', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER']+filename)
        Filename = text_helper.pdf2images(app.config['UPLOAD_FOLDER']+filename)
        Output = text_helper.ImagetoText(Filename)
        file_ocr = open("ocr_file.txt","wt")
        file_ocr.write(str(Output))
        file_ocr.close()
        return jsonify(Output)
        return "OCR DONE"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action="ocr">
        <input type=file name=file>
        <input type=submit value=Upload>
    </form> '''

@app.route('/uploads/<name>')
def download_file(name):

    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/')
def index():
    return "Record not found", status.HTTP_400_BAD_REQUEST
@app.route('/<number>')
def add(number):
    return f'<h1>Sorry there is no page avaible with this name {number}</h1>'

if __name__ == '__main__':
    app.run(debug=True)
