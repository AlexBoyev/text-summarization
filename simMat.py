import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity


class Mat:
    def __init__(self):
        self.sim_mat = []
        self.scores = []

    # creates similarity matrix using the original sentences and sentences' vectors
    def createMat(self, sentences, sentence_vectors):
        self.sim_mat = np.zeros([len(sentences), len(sentences)])

        for i in range(len(sentence_vectors)):
            for j in range(len(sentence_vectors)):
                if i != j:
                    self.sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 200), sentence_vectors[j].reshape(1, 200))[0, 0]

    def getSimMat(self):
        return self.sim_mat

    # ranks the sentences by creating graph and using "PageRank" algorithm
    def rank(self):
        nx_graph = nx.from_numpy_array(self.sim_mat)
        self.scores = nx.pagerank(nx_graph)

    def getScores(self):
        return self.scores


