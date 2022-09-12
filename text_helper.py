
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from pdf2image import convert_from_path
import glob
import base64
import json
import os
import datetime
import re
from natsort import natsorted

def pdf2images(path):
    filename = os.path.basename(path).split('.')[0]
    # print(filename)
    try:
        os.mkdir(filename)
    except:
        pass
    pages = convert_from_path(path, 350)
    i=1  
    for page in pages:        
        image_name_1 = f'./{filename}/page{i}.png'        
        page.save(image_name_1, "PNG")
        i = i+1  
    return filename

def ImagetoText(filename):
    images = glob.glob(f'{filename}/*', recursive=True)
    img=natsorted(images)
    # result_dict = {"documentId":filename}
    result_dict = {}
    # print(images)
    custom_config = "-c tessedit_create_tsv=1"
    # result_dict[filename]={}
    x=[]
    # count=0
    start = datetime.datetime.now()
    for k,image in enumerate(img):
        # count = count+1
        Page_text = {}
        # page_num = "page_num_" + str(count)
        # result_dict[filename][page_num] = {}
        image = cv2.imread(image,1)   
        d = pytesseract.image_to_string(image, lang="eng", config= custom_config)
        Page_text['page_num']= k+1
        Page_text['content']= d  
        # result_dict[filename][page_num]["content"] = d
        x.append(Page_text)
    result_dict['text'] = x
    end = datetime.datetime.now()
    result_dict['time taken'] = str(end-start)
    print(result_dict) 
    return result_dict


