from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocessing import preprocess_text
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'dataset'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)

        # =========================
        # PREPROCESSING
        # =========================
        df['sentimen'] = df['sentimen'].astype(str).str.lower().str.strip()
        df['clean'] = df['komentar'].astype(str).apply(preprocess_text)

        # =========================
        # TF-IDF + MODEL
        # =========================
        tfidf = TfidfVectorizer()
        X = tfidf.fit_transform(df['clean'])
        y = df['sentimen']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = MultinomialNB()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # =========================
        # GRAFIK SENTIMEN
        # =========================
        sentiment_count = df['sentimen'].value_counts()

        plt.figure(figsize=(6, 4))
        sentiment_count.plot(kind='bar')
        plt.title('Grafik Sentimen')
        plt.xlabel('Sentimen')
        plt.ylabel('Jumlah')

        chart_path = 'static/charts/chart.png'
        plt.savefig(chart_path)
        plt.close()

        # =========================
        # WORDCLOUD FUNCTION
        # =========================
        def safe_wordcloud(text, path):
            if not text.strip():
                text = "kosong"

            wc = WordCloud(
                width=800,
                height=400,
                background_color='white'
            ).generate(text)

            wc.to_file(path)

        # =========================
        # BUAT TEXT PER SENTIMEN
        # =========================
        positif_text = " ".join(
            df[df['sentimen'].str.contains("positif", na=False)]['clean']
        )

        negatif_text = " ".join(
            df[df['sentimen'].str.contains("negatif", na=False)]['clean']
        )

        netral_text = " ".join(
            df[df['sentimen'].str.contains("netral", na=False)]['clean']
        )

        # =========================
        # WORDCLOUD SAVE
        # =========================
        safe_wordcloud(positif_text, 'static/wordcloud/positif.png')
        safe_wordcloud(negatif_text, 'static/wordcloud/negatif.png')
        safe_wordcloud(netral_text, 'static/wordcloud/netral.png')

        # =========================
        # DATA TABLE
        # =========================
        hasil = df[['komentar', 'sentimen']].head(20).values.tolist()

        return render_template(
            'hasil.html',
            accuracy=round(accuracy * 100, 2),
            tables=hasil,
            chart=chart_path
        )


if __name__ == '__main__':
    print("RUNNING FLASK...")
    app.run(debug=True, port=5001)