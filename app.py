from flask import Flask, render_template, request
import os
import pandas as pd
import qrcode


# Database
from config import conn, cursor


# NLP
from models.preprocessing import preprocess_text
from models.sentiment_model import predict_sentiment
from models.wordcloud_generator import generate_wordcloud
from models.insight_ai import generate_insight



app = Flask(__name__)




# =========================
# Folder
# =========================


UPLOAD_FOLDER = "static/uploads"

QR_FOLDER = "static/qrcode"


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(QR_FOLDER, exist_ok=True)




# menyimpan nama kolom upload terakhir

nama_kolom_global = "Komentar"





# =========================
# Dashboard
# =========================


@app.route('/')

def dashboard():


    url = request.host_url



    qr_path = os.path.join(

        QR_FOLDER,

        "ngrok_qr.png"

    )



    img = qrcode.make(url)

    img.save(qr_path)



    return render_template(

        "dashboard.html"

    )







# =========================
# Upload
# =========================


@app.route('/upload', methods=['POST'])

def upload():


    global nama_kolom_global



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



        # =====================
        # Baca File
        # =====================


        if file.filename.endswith(".csv"):


            df = pd.read_csv(filepath)



        elif file.filename.endswith((".xlsx",".xls")):


            df = pd.read_excel(filepath)



        else:


            return "File harus CSV atau Excel"






        # =====================
        # Cari kolom teks
        # =====================


        kolom_teks = None



        for kolom in df.columns:


            if df[kolom].dtype == "object":


                kolom_teks = kolom


                break





        if kolom_teks is None:


            return "Tidak ditemukan kolom teks"





        # simpan nama kolom asli


        nama_kolom_global = kolom_teks






        # =====================
        # Hapus data lama
        # =====================


        cursor.execute(

            "DELETE FROM hasil_sentimen"

        )


        conn.commit()







        # =====================
        # NLP
        # =====================


        for data in df[kolom_teks].dropna():



            teks = str(data)



            preprocessing = preprocess_text(

                teks

            )



            sentimen = predict_sentiment(

                preprocessing

            )





            cursor.execute("""


            INSERT INTO hasil_sentimen

            (

            komentar,

            preprocessing,

            sentimen

            )


            VALUES

            (?,?,?)


            """,

            (

            teks,

            preprocessing,

            sentimen


            ))







        conn.commit()






        generate_wordcloud()






        # =====================
        # Statistik
        # =====================


        total = len(df)



        cursor.execute("""


        SELECT COUNT(*)

        FROM hasil_sentimen

        WHERE sentimen='Positif'


        """)


        positif = cursor.fetchone()[0]






        cursor.execute("""


        SELECT COUNT(*)

        FROM hasil_sentimen

        WHERE sentimen='Negatif'


        """)


        negatif = cursor.fetchone()[0]






        cursor.execute("""


        SELECT COUNT(*)

        FROM hasil_sentimen

        WHERE sentimen='Netral'


        """)


        netral = cursor.fetchone()[0]








        return render_template(


            "hasil.html",


            total=total,


            positif=positif,


            negatif=negatif,


            netral=netral


        )







    except Exception as e:


        return f"Terjadi kesalahan: {e}"









# =========================
# Hasil
# =========================


@app.route('/hasil')

def hasil():


    cursor.execute(

        "SELECT COUNT(*) FROM hasil_sentimen"

    )


    total = cursor.fetchone()[0]




    cursor.execute("""


    SELECT COUNT(*)

    FROM hasil_sentimen

    WHERE sentimen='Positif'


    """)


    positif = cursor.fetchone()[0]




    cursor.execute("""


    SELECT COUNT(*)

    FROM hasil_sentimen

    WHERE sentimen='Negatif'


    """)


    negatif = cursor.fetchone()[0]




    cursor.execute("""


    SELECT COUNT(*)

    FROM hasil_sentimen

    WHERE sentimen='Netral'


    """)


    netral = cursor.fetchone()[0]





    return render_template(


        "hasil.html",


        total=total,


        positif=positif,


        negatif=negatif,


        netral=netral


    )









# =========================
# Grafik
# =========================


@app.route('/grafik')

def grafik():


    cursor.execute("""


    SELECT sentimen,

    COUNT(*)

    FROM hasil_sentimen

    GROUP BY sentimen


    """)



    data = cursor.fetchall()



    labels=[]

    values=[]




    for row in data:


        labels.append(row[0])

        values.append(row[1])





    return render_template(

        "grafik.html",

        labels=labels,

        values=values

    )









# =========================
# WordCloud
# =========================


@app.route('/wordcloud')

def wordcloud():


    return render_template(

        "wordcloud.html"

    )









# =========================
# Tabel
# =========================


@app.route('/tabel')

def tabel():


    cursor.execute("""


    SELECT

    komentar,

    preprocessing,

    sentimen


    FROM hasil_sentimen


    """)



    hasil = cursor.fetchall()





    return render_template(


        "tabel.html",


        hasil=hasil,


        nama_kolom=nama_kolom_global


    )









# =========================
# Insight AI
# =========================


@app.route('/insight')

def insight():


    hasil_ai = generate_insight()



    return render_template(


        "insight.html",


        insight=hasil_ai


    )

# =========================
# Run
# =========================


if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5050,

        debug=True

    )