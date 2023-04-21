from flask import Flask, request, render_template
from gensim.models import Word2Vec
from utils.predict import pred
from utils.get_vector import vector_w2v
from utils.visualisasi import viz_pie
import joblib
import pandas as pd

model_svm = joblib.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\machine_learning\svm_w2v_skipgram.joblib')
model_w2v = Word2Vec.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\word_embeddings\w2v_skipgram.model')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentimen', methods=['POST'])
def analisis_sentiment():
    sentence = request.form['sentence']
    df = pd.DataFrame({'Text': [sentence]})
    predict, proba = pred(df, vector_w2v, model_w2v, model_svm)
    probability = [proba[0][1] if predict[0] == 'Positif' else proba[0][0]]
    return render_template('index.html', predict=predict[0], probability=probability[0], sentence=sentence)

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

    df['Label'], proba = pred(df, vector_w2v, model_w2v, model_svm)
    df['Proba Positif'] = [round(i[1],5) for i in proba]
    df = df.drop_duplicates(subset='Text')
    
    viz = viz_pie(df)
    return render_template('hasil_analisis.html',df=df, chart_data=viz)

if __name__ == '__main__': 
    app.run()
