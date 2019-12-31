# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 21:11:06 2019

@author: Ashwin Ram1
"""

import os
import tensorflow as tf
import re
import joblib

from flask import Flask, request, url_for, Response
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import simplejson as json
import numpy as np
import argparse
import imutils
import cv2
import time
import uuid
import base64
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2



app = Flask(__name__)


@app.route('/line', methods=['GET', 'POST'])

def upload_line():
    if request.method == 'POST':
        # file = request.files['image']
        name = request.form.get('name')
        name = str(name)
        print(name)
        t = name.split(" ")
        t=[t]
        t = str(t)
        t = [t]
        pred = pipe1.predict_prob(t)
        
        

        # for i in pred:
            
        result = np.argmax(pred)
        result=int(result)
        print(result)
        
        
        data = {

                'result': result



            }

        js = json.dumps(data)
        res = Response(js, status=200, mimetype='application/json')
        return res


@app.route('/', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file_path = os.path.join("./", filename)
        
        file.save(file_path)
        img = cv2.imread(file_path)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        img = cv2.medianBlur(img, 3)
        cv2.threshold(img,127,255,cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(img)

        print(text)

        cor = {
            0: 'analysis',
            1: 'application',
            2: 'comprehension',
            3: 'evaluation',
            4: 'knowledge',
            5: 'synthesis',
        }

        r = {
             'analysis': 0,
             'application': 0,
         'comprehension': 0,
             'evaluation': 0,
             'knowledge': 0,
             'synthesis': 0,
            
        }

        for i in text.split("\n"):
            
            if (i != ""):
                
                s=i
                data = re.sub("\d+. ", "", s)
                t = data.split(" ")
                
                t=[t]
                t = str(t)
                t = [t]
                pred = pipe1.predict_proba(t)
                
                resu = np.argmax(pred)
                print(resu)

                resu=int(resu)
                res = cor[resu]
                r[res]=r[res]+1
                
        for key in r:
            r[key]=((r[key])/len(text.split("\n")))*100
        
                
        print(r)    





        js = json.dumps(r)
        res = Response(js, status=200, mimetype='application/json')
        return res





if __name__ == "__main__":
    pipe1 = joblib.load("filename.pkl")
    

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    app.run(host="localhost",port=8000,debug=True)