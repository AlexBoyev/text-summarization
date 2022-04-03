import io
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

import prep
import vec
import simMat

p = prep.preprocessing()
v = vec.Vector()
sim = simMat.Mat()
min_sen = 0


# gets the number of sentences in the article
def get_sen_num():
    sn = senNum.get()

    if sn.isdigit():
        sn_int = int(sn)
        if sn_int is 0:
            return False
        else:
            return sn_int
    else:
        return False


# gets the rank of the sentences from the similarity matrix, sorts them and writes them into a file
def ranked(sen):
    sim.rank()
    ranked_sentences = sorted(((sim.getScores()[i], s) for i, s in enumerate(p.getSentences())), reverse=True)

    with io.open('summarization.txt', "w", encoding="utf-8") as f:
        for i in range(sen):
            f.write("%s\n" % ranked_sentences[i][1])


# opens the wanted file
def browse():
    file_name = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"), ("pdf files","*.pdf")))
    entry.delete(0, END)
    entry.insert(0, file_name)
    p.read_file_to_list(file_name)


def preprocess():
    global min_sen

    p.read_structure()  # reads the file

    progress['value'] = 25
    top.update_idletasks()

    v.createVector(p.getWholeFile())  # creates word vectors

    progress['value'] = 50
    top.update_idletasks()

    sim.createMat(p.getSentences(), v.getSentence_vectors())  # creates the similarity matrix

    progress['value'] = 75
    top.update_idletasks()

    article_len = p.getArticle_len()
    min_sen = int(article_len * 0.1)

    s = "The recommended number of sentences for best summarization results is: " + str(min_sen)
    messagebox.showinfo("Message", s)


def summarize():
    sen = get_sen_num()
    if sen is False:
        messagebox.showinfo("Message", "Number of sentences must be a positive integer bigger than 0")
    else:
        ranked(sen)

        progress['value'] = 100
        top.update_idletasks()

        messagebox.showinfo("Message", "Summarization completed")


# main window
top = tkinter.Tk()
top.title('Extractive summarization')
top.geometry("600x400")

# file path label
lb1 = Label(top, text="File path:")
lb1.pack()

# file path text box
entry = Entry(top, width=60)
entry.pack(side=TOP, padx=10, pady=10)

# browse button
BrowseButton = tkinter.Button(top, text ="Browse", command = browse)
BrowseButton.pack(side=TOP, padx=10, pady=10)

# preprocess button
preprocessButton = tkinter.Button(top, text ="Preprocess", command = preprocess)
preprocessButton.pack(side=TOP, padx=10, pady=10)

# number of sentences label
lb2 = Label(top, text="Enter number of sentences:")
lb2.pack()

# desired number of sentences text box
senNum = Entry(top, width=10)
senNum.pack(side=TOP, padx=10, pady=10)

# summarize button
SummarizeButton = tkinter.Button(top, text ="Summarize", command = summarize)
SummarizeButton.pack(side=TOP, padx=10, pady=10)

# progress bar
progress = Progressbar(top, orient=HORIZONTAL, length=200, mode='determinate')
progress.pack(side=TOP, padx=10, pady=20)


top.mainloop()
