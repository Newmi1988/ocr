import argparse
import os

import cv2
import pytesseract
from flask import Flask
from flask_restx import Api, Resource
from PIL import Image
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = './tmp/tmp.png'

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)
 
@api.route('/info')
class Info(Resource):
    def get(self):
        return {'Tesseract Api': 'v0.0.1'}

@api.route('/analyse')
@api.expect(upload_parser)
class Tesserace(Resource):

    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file'] 

        uploaded_file.save(UPLOAD_FOLDER)

        image = cv2.imread(UPLOAD_FOLDER)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # preprocess with blur
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # preprocess with blur
        # gray = cv2.medianBlur(gray, 3)

        filename = './tmp/tmp_proc.png'
        cv2.imwrite(filename, gray)
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)

        return {'text' : text}

