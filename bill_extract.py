"""
Author: Fiqri Wicaksono
"""

from PIL import Image 
import pytesseract 
from pdf2image import convert_from_path 
import os 
import json

home = os.getcwd()
# the path of the electricity bill file
img_path = os.path.join(home, 'electricity_bill.pdf') 

"""
This program extract information from given electricity bill template in pdf format and 
wrap it up in json file, to extract different template some modification(s) are necessary.
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

def extract_attribute(txt_list):
    # extract the bill's attributes
    for txt in txt_list:
        if txt[:7].isdigit():
            return txt.split()

def extract_bill(txt_list):
    # extract bill's payment
    pay_list = list()
    for txt in txt_list:
        if txt[-1].isdigit() and txt[-4:]!='2020':
            pay_list.append(txt)
    return pay_list

def jsonwrap(pay_list, attribute):
    # wrap the extracted informations as json
    bill = {}
    summary = {}
    for pay in pay_list[:5]:
        pay = pay.split()
        summary[' '.join(pay[:-1])] = float(pay[-1].replace(',',''))
    detail = {}
    for pay in pay_list[5:]:
        pay = pay.split()
        detail[' '.join(pay[:-1])] = float(pay[-1].replace(',',''))
    attr = {}
    attr['Invoice No.'] = attribute[0]
    attr['Account No.'] = attribute[1]
    attr['Amount Due'] = attribute[2]
    attr['Payment Due'] = attribute[3]
    bill['Bill Summary'] = summary
    bill['Bill Details'] = detail
    bill['Bill Attributes'] = attr
    with open('bill_extracted.json', 'w') as outfile:
        json.dump(bill, outfile)
    print('json file generated!')

def cleanup():
    # clean up the converted pdf
    cnt = 0
    for r, d, f in os.walk(home):
        for file in f:
            if '.jpg' in file:
                os.remove(file)
                cnt += 1
    print(f'{str(cnt)} image files cleaned')

def main():
    to_img(img_path)
    txt_list = read_img()
    attribute = extract_attribute(txt_list)
    pay_list = extract_bill(txt_list)
    jsonwrap(pay_list, attribute)
    cleanup()

if __name__ == '__main__':
    main()