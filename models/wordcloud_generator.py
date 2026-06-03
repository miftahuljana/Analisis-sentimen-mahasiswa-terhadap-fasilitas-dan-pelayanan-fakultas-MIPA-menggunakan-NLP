from wordcloud import WordCloud
import sqlite3
import os

def generate_wordcloud():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    os.makedirs(
        'static/wordcloud',
        exist_ok=True
    )

    sentiments = [
        'Positif',
        'Negatif',
        'Netral'
    ]

    for sentimen in sentiments:

        cursor.execute("""
        SELECT preprocessing
        FROM hasil_sentimen
        WHERE sentimen=?
        """, (sentimen,))

        data = cursor.fetchall()

        print(sentimen)
        print(data)

        text = " ".join(
            [str(row[0]) for row in data]
        )

        print(text)

        if len(text) > 0:

            wc = WordCloud(
                width=800,
                height=400,
                background_color='white'
            ).generate(text)

            file_path = f"static/wordcloud/{sentimen.lower()}.png"

            wc.to_file(file_path)

            print("TERSIMPAN :", file_path)

    conn.close()