import joblib
from gensim.models import Word2Vec

model_svm = joblib.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\machine_learning\svm_w2v_skipgram.joblib')
model_w2v = Word2Vec.load('D:\KULIAH\Semester 8\Skripsi\Deploy Model\model\word_embeddings\w2v_skipgram.model')
