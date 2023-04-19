import numpy as np

def vector_w2v(sentence, model):
    tokens = sentence.split()
    vector = np.mean([model.wv[token] for token in tokens if token in model.wv], axis=0)
    return vector

def vector_fasttext(sentence, model):
    tokens = sentence.split()
    vector = np.mean([model.wv[token] for token in tokens], axis=0)
    return vector
