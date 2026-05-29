# 📊 Analisis Sentimen Mahasiswa terhadap Fasilitas dan Pelayanan Fakultas MIPA
Website ini merupakan aplikasi Analisis Sentimen berbasis Web yang dibuat menggunakan Python Flask + Machine Learning (Naive Bayes) + NLP (TF-IDF).
Project ini digunakan untuk menganalisis opini mahasiswa terhadap fasilitas dan pelayanan di Fakultas MIPA.

🚀 Fitur
Upload dataset komentar mahasiswa (CSV)
Preprocessing teks menggunakan NLP
Klasifikasi sentimen (Positif, Negatif, Netral)
Model Machine Learning (Naive Bayes)

Visualisasi data:
Menampilkan hasil akurasi model
Grafik distribusi sentimen
WordCloud setiap sentimen
Tampilan hasil analisis dalam web

🛠️ Teknologi yang Digunakan
Python
Flask
Pandas
Scikit-Learn
Matplotlib
WordCloud
NLP Preprocessing (custom preprocessing.py)

⚙️ Cara Menjalankan Project
1. Install Python & Laragon (opsional)

Pastikan Python sudah terinstall di komputer.

2. Install library yang dibutuhkan

Jalankan di terminal:

pip install flask pandas scikit-learn sastrawi matplotlib wordcloud
python.exe -m pip install --upgrade pip   

3. Jalankan project

Masuk ke folder project:

cd sentiment-mipa  

Lalu jalankan:
python app.py

4. Buka di browser
http://127.0.0.1:5001/

📂 Format Dataset

File CSV harus memiliki kolom:

komentar                        sentimen
Ruang kelas nyaman	            positif
Wifi sering error	              negatif

📊 Output Sistem

Setelah upload dataset, sistem akan menghasilkan:

🎯 Akurasi model Naive Bayes
📈 Grafik distribusi sentimen
☁️ WordCloud Positif, Negatif, Netral
📋 Data hasil klasifikasi

🎯 Tujuan Project

Project ini dibuat untuk:

Menganalisis opini mahasiswa terhadap fasilitas kampus
Mengimplementasikan NLP dalam studi kasus nyata
Menerapkan Machine Learning (Naive Bayes)
Membuat sistem analisis berbasis web

👨‍💻 Catatan
Project ini masih bisa dikembangkan lebih lanjut seperti:

Dashboard interaktif
Export laporan PDF
Database MySQL
Login admin
