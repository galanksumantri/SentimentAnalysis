import pandas as pd
import re

kamus_slang = pd.read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')

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