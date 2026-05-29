import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

stop_factory = StopWordRemoverFactory()
stopwords = stop_factory.create_stop_word_remover()

def preprocess_text(text):

    # lowercase
    text = text.lower()

    # hapus angka
    text = re.sub(r'\d+', '', text)

    # hapus tanda baca
    text = re.sub(r'[^\w\s]', '', text)

    # hapus spasi berlebih
    text = text.strip()

    # stopword removal
    text = stopwords.remove(text)

    # stemming
    text = stemmer.stem(text)

    return text