from flask import Flask, request, render_template
from gensim.models import Word2Vec
from utils.preprocessing import *
from utils.get_vector import *
import pandas as pd
import numpy as np
import joblib

model_svm = joblib.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\machine_learning\svm_w2v_skipgram.joblib')
model_w2v = Word2Vec.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\word_embeddings\w2v_skipgram.model')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentimen', methods=['POST'])
def word_similarity():
    SENTENCE = request.form['sentence']
    df = pd.DataFrame({'Text': [SENTENCE]})
    df['Text'] = df['Text'].apply(caseFolding).apply(filtering).apply(convert_slang, kamus_slang=kamus_slang)
    vector = [vector_w2v(sentence, model_w2v) for sentence in df['Text']]
    predict = model_svm.predict(vector)
    proba = model_svm.predict_proba(vector)[0]
    probability = [proba[1] if predict[0] == 'Positif' else proba[0]]
    return render_template('index.html', predict=predict[0], probability=probability[0], sentence=SENTENCE)

if __name__ == '__main__': 
    app.run(debug=True)
