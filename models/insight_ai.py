import sqlite3

def generate_insight():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sentimen, COUNT(*)
        FROM hasil_sentimen
        GROUP BY sentimen
    """)

    data = cursor.fetchall()
    conn.close()

    positif = 0
    negatif = 0
    netral = 0

    for row in data:
        if row[0] == "Positif":
            positif = row[1]
        elif row[0] == "Negatif":
            negatif = row[1]
        elif row[0] == "Netral":
            netral = row[1]

    total = positif + negatif + netral

    if total == 0:
        return "Belum ada data yang dianalisis."

    persen_positif = round((positif/total)*100,2)
    persen_negatif = round((negatif/total)*100,2)
    persen_netral = round((netral/total)*100,2)

    insight = f"""
Berdasarkan analisis terhadap {total} komentar mahasiswa:

- Sentimen Positif : {persen_positif}%
- Sentimen Negatif : {persen_negatif}%
- Sentimen Netral : {persen_netral}%

"""

    if positif > negatif:
        insight += """
Mayoritas mahasiswa memberikan penilaian POSITIF terhadap fasilitas dan pelayanan Fakultas MIPA.

Rekomendasi: Pertahankan kualitas layanan yang sudah baik.
"""
    else:
        insight += """
Sentimen NEGATIF masih cukup tinggi.

Rekomendasi: Perlu evaluasi fasilitas dan pelayanan yang dikeluhkan mahasiswa.
"""

    return insight