# Electricity Bill Extractor
 This program extract information from given electricity bill template in pdf format and wrap it up in json file, to extract different template some modification(s) are necessary.
## Dependencies
- Python 3, Tesseract OCR, & Poppler
- To install the required packages, run `pip install -r requirements.txt`
## Getting Started
- First, clone the repository and enter the folder directory
`git clone https://github.com/fiqriwicaksono/Electricity-Bill-Extractor`
`cd Electricity-Bill-Extractor`
- Then run the code
`python3 bill_extract.py`
- The program will extract the pdf's information using OCR algorithm and wrap the output in a json file.
![alt text](https://raw.githubusercontent.com/fiqriwicaksono/Electricity-Bill-Extractor/master/img/output.png)
