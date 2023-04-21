from .preprocessing import * 

kamus_slang = pd.read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')

def pred(df, emb, model_emb, model_ml):
    df['Text Clean'] = df['Text'].apply(caseFolding).apply(filtering).apply(convert_slang, kamus_slang=kamus_slang)
    vector = [emb(sentence, model_emb) for sentence in df['Text Clean']]
    predict = model_ml.predict(vector)
    proba = model_ml.predict_proba(vector)
    
    return predict, proba
