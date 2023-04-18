from flask import Flask, request, render_template
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import joblib
import re

model_svm = joblib.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\machine_learning\svm_w2v_skipgram.joblib')
model_w2v = Word2Vec.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\word_embeddings\w2v_skipgram.model')
kamus_slang = pd.read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')

app = Flask(__name__)

def caseFolding(data):
  return data.lower()

def filtering(data):
  # Menghapus hashtag
  string = re.sub(r'#\w+', '', data)
  # Menghapus kata berawalan @
  string = re.sub('@[^\s]+','',string)
  # Menghapus tanda baca dan angka
  string = re.sub(f"[^a-zA-Z]", ' ', string)
  # Menghapus Emoji
  emoj = re.compile("["
      u"\U0001F600-\U0001F64F"  # emoticons
      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
      u"\U0001F680-\U0001F6FF"  # transport & map symbols
      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
      u"\U00002500-\U00002BEF"  # chinese char
      u"\U00002702-\U000027B0"
      u"\U00002702-\U000027B0"
      u"\U000024C2-\U0001F251"
      u"\U0001f926-\U0001f937"
      u"\U00010000-\U0010ffff"
      u"\u2640-\u2642" 
      u"\u2600-\u2B55"
      u"\u200d"
      u"\u23cf"
      u"\u23e9"
      u"\u231a"
      u"\ufe0f"  # dingbats
      u"\u3030"
                    "]+", re.UNICODE)
  string = re.sub(emoj, '', string)
  # Menghapus kata dengan 1 karakter
  string = string.split()
  string = [k for k in string if len(re.sub(r'\W+', '', k)) > 1]
  return ' '.join(string)

def convert_slang(data, kamus_slang):
    kata_kalimat = data.split() 
    kata_baru = [] 
    for kata in kata_kalimat:
        if kata in kamus_slang['slang'].values:
            kata_baru.append(kamus_slang.loc[kamus_slang['slang'] == kata, 'formal'].values[0])
        else:
            kata_baru.append(kata)
    kalimat_baru = ' '.join(kata_baru)
    return kalimat_baru

def get_sentence_vector_w2v(sentence, model):
    tokens = sentence.split()
    vector = np.mean([model.wv[token] for token in tokens if token in model.wv], axis=0)
    return vector

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentimen', methods=['POST'])
def word_similarity():
    SENTENCE = request.form['sentence']
    df = pd.DataFrame({'Text': [SENTENCE]})
    df['Text'] = df['Text'].apply(caseFolding).apply(filtering).apply(convert_slang, kamus_slang=kamus_slang)
    vector = [get_sentence_vector_w2v(sentence, model_w2v) for sentence in df['Text']]
    predict = model_svm.predict(vector)
    proba = model_svm.predict_proba(vector)[0]
    probability = [proba[1] if predict[0] == 'Positif' else proba[0]]
    return render_template('index.html', predict=predict[0], probability=probability[0])

if __name__ == '__main__': 
    app.run()