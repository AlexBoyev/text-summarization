import numpy as np


class Vector:
    def __init__(self):
        self.word_embeddings = {}
        self.sentence_vectors = []

    # loads the word embeddings vectors from the GloVe file and processes them
    def wordEmbedding(self):
        f = open('glove.6B.200d.txt', encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            self.word_embeddings[word] = coefs
        f.close()

    # creates vectors of words from the article, based on the GloVe vectors
    def createVector(self, clean_sentences):
        self.wordEmbedding()
        for i in clean_sentences:
            if len(i) != 0:
                v = sum([self.word_embeddings.get(w, np.zeros((200,))) for w in i.split()]) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((200,))
            self.sentence_vectors.append(v)

    def getSentence_vectors(self):
        return self.sentence_vectors

