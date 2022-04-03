import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import docx
from pdfminer.layout import LAParams
from io import StringIO
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from tkinter import *
from tkinter import messagebox as mb
import os


class preprocessing:

    def __init__(self):
        self.WholeFile = []
        self.sentences = []
        self.article_len = []

    # stores the entered directory for the needed files
    def read_file_to_list(self, path_name):
        global filename

        filename = path_name

    # verifies that the file is not empty
    def is_empty(self, file):
        if os.stat(file).st_size == 0:
            return True
        return False

    # reads the file and gets it ready for preprocessing
    def read_structure(self):
        global text

        try:
            # if the file is .txt
            if filename.endswith('.txt'):
                with open(filename, 'r') as structure_file:
                    content = structure_file.read()

                # cleans the extra new-lines
                temp = re.sub(r'(\n\s*)+\n+', '\n', content)
                self.sentences = temp
                self.WholeFile = temp

                structure_file.close()

            # if the file is .pdf
            elif filename.endswith('.pdf'):
                rsrcmgr = PDFResourceManager()
                retstr = StringIO()
                codec = 'utf-8'
                laparams = LAParams()
                device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
                fp = open(filename, 'rb')
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)
                text = retstr.getvalue()
                fp.close()
                device.close()
                retstr.close()

                # cleans the extra new-lines
                temp = re.sub(r'(\n\s*)+\n+', '\n', text)
                self.sentences = temp
                self.WholeFile = temp

            # if the file is .docx
            elif filename.endswith('.docx'):
                doc = docx.Document(filename)
                fullText = ''
                for para in doc.paragraphs:
                    fullText += para.text
                    self.WholeFile = fullText
                self.sentences = self.WholeFile

            # gets the text file into a list of lists (words inside sentences)
            lst = []
            str = ''
            stop_words = set(stopwords.words('english'))

            text = re.sub(r'-\n(\w+ *)', r'\1\n', self.WholeFile)
            lst = sent_tokenize(text)
            self.article_len = len(lst)
            self.sentences = lst

            # removes punctuations, numbers and special characters
            self.WholeFile = pd.Series(self.sentences).str.replace("[^a-zA-Z]", " ")
            # makes alphabets lowercase
            self.WholeFile = [s.lower() for s in self.WholeFile]

            # removes stopwords
            def remove_stopwords(sen):
                sen_new = " ".join([i for i in sen if i not in stop_words])
                return sen_new

            self.WholeFile = [remove_stopwords(r.split()) for r in self.WholeFile]

            with io.open('filtered.txt', "w", encoding="utf-8") as f:
                for item in self.WholeFile:
                    f.write("%s\n" % item)

            return self.WholeFile

        except:
            mb.showinfo("Error")
            raise

    def getWholeFile(self):
        return self.WholeFile

    def getSentences(self):
        return self.sentences

    def getArticle_len(self):
        return self.article_len
