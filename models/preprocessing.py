import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopword = StopWordRemoverFactory().create_stop_word_remover()

def preprocess_text(text):

    text = str(text)

    # lowercase
    text = text.lower()

    # hapus url
    text = re.sub(r'http\S+', '', text)

    # hapus angka
    text = re.sub(r'\d+', '', text)

    # hapus karakter khusus
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()

    # stopword
    text = stopword.remove(text)

    # stemming
    text = stemmer.stem(text)

    return text