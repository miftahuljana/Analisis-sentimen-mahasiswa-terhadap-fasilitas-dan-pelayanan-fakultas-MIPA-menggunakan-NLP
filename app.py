from flask import Flask, render_template, request
import os
import pandas as pd
import qrcode
from flask import request

# Database
from config import conn, cursor

# NLP
from models.wordcloud_generator import generate_wordcloud
from models.preprocessing import preprocess_text
from models.sentiment_model import predict_sentiment
from models.insight_ai import generate_insight


app = Flask(__name__)

# =========================
# Folder Upload
# =========================

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# Dashboard
# =========================

@app.route('/')
def dashboard():

    url = request.host_url  # otomatis ngrok / localhost

    import qrcode
    import os

    path = "static/qrcode"
    os.makedirs(path, exist_ok=True)

    img = qrcode.make(url)
    img.save(os.path.join(path, "ngrok_qr.png"))

    return render_template('dashboard.html')


# =========================
# Upload & Analisis
# =========================

@app.route('/upload', methods=['POST'])
def upload():

    if 'dataset' not in request.files:
        return "File tidak ditemukan"

    file = request.files['dataset']

    if file.filename == '':
        return "Pilih file terlebih dahulu"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    try:

        # Baca CSV
        df = pd.read_csv(filepath)

        # Pastikan kolom komentar ada
        if 'komentar' not in df.columns:
            return "Kolom 'komentar' tidak ditemukan pada file CSV"

        hasil = []

        # Hapus data lama
        cursor.execute("DELETE FROM hasil_sentimen")
        conn.commit()

        # Proses semua komentar
        for komentar in df['komentar']:

            clean_text = preprocess_text(komentar)

            sentimen = predict_sentiment(clean_text)

            # Simpan ke database
            cursor.execute("""
                INSERT INTO hasil_sentimen
                (
                    komentar,
                    preprocessing,
                    sentimen
                )
                VALUES (?, ?, ?)
            """,
            (
                komentar,
                clean_text,
                sentimen
            ))

            hasil.append({
                'komentar': komentar,
                'preprocessing': clean_text,
                'sentimen': sentimen
            })

        conn.commit()
        generate_wordcloud()

        # Setelah analisis selesai
        return render_template('hasil.html')

    except Exception as e:
        return f"Terjadi kesalahan: {e}"


# =========================
# Halaman Hasil
# =========================

@app.route('/hasil')
def hasil():
    insight = generate_insight()
    return render_template('hasil.html', insight=insight)


# =========================
# Grafik
# =========================

@app.route('/grafik')
def grafik():

    cursor.execute("""
        SELECT sentimen,
               COUNT(*) as jumlah
        FROM hasil_sentimen
        GROUP BY sentimen
    """)

    data = cursor.fetchall()

    labels = []
    values = []

    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return render_template(
        'grafik.html',
        labels=labels,
        values=values
    )


# =========================
# WordCloud
# =========================

@app.route('/wordcloud')
def wordcloud():

    return render_template(
        'wordcloud.html'
    )


# =========================
# Tabel Hasil
# =========================

@app.route('/tabel')
def tabel():

    cursor.execute("""
        SELECT komentar,
               preprocessing,
               sentimen
        FROM hasil_sentimen
    """)

    hasil = cursor.fetchall()

    return render_template(
        'tabel.html',
        hasil=hasil
    )


# =========================
# Insight AI
# =========================

@app.route('/insight')
def insight():

    hasil_insight = generate_insight()

    return render_template(
        'insight.html',
        insight=hasil_insight
    )


# =========================
# Jalankan Flask
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)