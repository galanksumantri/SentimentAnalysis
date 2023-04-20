from flask import Flask, request, render_template
from gensim.models import Word2Vec
from utils.preprocessing import *
from utils.get_vector import *
import matplotlib.pyplot as plt
import matplotlib, io, base64, joblib
import pandas as pd
import numpy as np

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

@app.route('/sentimen_file')
def sentimen_file():
    return render_template('sentimen_file.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        return "Jenis file tidak didukung."

    df['Text_clean'] = df['Text'].apply(caseFolding).apply(filtering).apply(convert_slang, kamus_slang=kamus_slang)
    vector = [vector_w2v(sentence, model_w2v) for sentence in df['Text_clean']]
    predict = model_svm.predict(vector)
    df['Label'] = predict
    
    sentiment_counts = df['Label'].value_counts()

    matplotlib.use('Agg')
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor('none')
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Analisis Sentimen')

    # Convert chart to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()

    return render_template('hasil_analisis.html',df=df, chart_data=chart_data)

if __name__ == '__main__': 
    app.run()
