"""
Author: Fiqri Wicaksono
"""

from PIL import Image 
import pytesseract 
from pdf2image import convert_from_path 
import os 
import json
import re

home = os.getcwd()
# the path of the electricity bill file
filename = 'electricity_bill.pdf'
pdf_path = os.path.join(home, filename)

"""
This program extract information from various bill template in pdf format and 
wrap it up in json file.
"""

def to_img(img_path):
    # convert the pdf file into jpg
    # feel free to tweak the dpi parameter for better output
    pages = convert_from_path(img_path, 200)
    imgs = 0
    for page in pages:
        imgs+=1
        filename = "page_"+str(imgs)+".jpg"
        page.save(filename, 'JPEG')
    print(f'{str(imgs)} image files generated')

def read_img():
    # extract the text from the image file
    files = list()
    # r=root, d=directories, f = files
    for r, d, f in os.walk(home):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
    files.sort()
    txt_list = list()
    for file in files:
        text = pytesseract.image_to_string(Image.open(file))
        text = text.split('\n')
        text = list(filter(lambda x: x.strip(), text))
        for txt in text:
            txt_list.append(txt)
    return txt_list

def extract_bill(txt_list):
    # extract bill's payment
    pay_list = [txt for txt in txt_list if re.search(r'(\.\d{2}$)|(\.\d{3}$)', txt)]
    return pay_list

def extract_attribute(txt_list, pay_list):
    # extract the bill's attributes
    attr_list = [txt for txt in txt_list if txt not in pay_list]
    return attr_list

def jsonwrap(pay_list, attr_list):
    # wrap the extracted informations as json
    bill = {}
    detail = {}
    for pay in pay_list:
        pay = pay.split()
        detail[' '.join(pay[:-1])] = pay[-1]
    bill['Bill Details'] = detail
    bill['Bill Attributes'] = attr_list
    with open(f'{filename}_extracted.json', 'w') as outfile:
        json.dump(bill, outfile)
    print('json file generated!')

def cleanup():
    # clean up the converted pdf
    cnt = 0
    for r, d, f in os.walk(home):
        for file in f:
            if '.jpg' in file:
                try:
                    os.remove(file)
                    cnt += 1
                except FileNotFoundError:
                    pass
    print(f'{str(cnt)} image files cleaned')

def main():
    to_img(pdf_path)
    txt_list = read_img()
    pay_list = extract_bill(txt_list)
    attr_list = extract_attribute(txt_list, pay_list)
    jsonwrap(pay_list, attr_list)
    cleanup()

if __name__ == '__main__':
    main()