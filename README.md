# Bike Sharing Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://abhiprayaa29-bike-sharing-dashboard-dashboarddashboard-j5y8xb.streamlit.app/)

Proyek akhir kelas **Belajar Analisis Data dengan Python** — Dicoding.

Dashboard interaktif untuk menganalisis pola permintaan penyewaan sepeda **Capital Bikeshare, Washington D.C.** periode **2011–2012** menggunakan **Bike Sharing Dataset**.

**Live Demo:** [Streamlit Community Cloud](https://abhiprayaa29-bike-sharing-dashboard-dashboarddashboard-j5y8xb.streamlit.app/)

**Nama:** Abdillah Abhipraya Abrar
**Email:** abdillahabhi13@gmail.com  
**ID Dicoding:** abhipraya29

---

## 1. Deskripsi Proyek

Proyek ini melakukan proses analisis data end-to-end: gathering data, assessing data, cleaning data, exploratory data analysis (EDA), visualisasi, analisis lanjutan berupa segmentasi permintaan (binning kuartil), hingga penyusunan kesimpulan dan rekomendasi action item. Hasil analisis disajikan dalam notebook dan dashboard Streamlit.

Dataset terdiri dari dua tingkat agregasi:

- **`data/day.csv`** — 731 baris data harian.
- **`data/hour.csv`** — 17.379 baris data per jam.
- **`data/Readme.txt`** — dokumentasi asli dataset.

Sumber data: [UCI Machine Learning Repository — Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) (Fanaee-T & Gama, 2013).

> Catatan: label musim mengikuti dokumentasi dataset (season 1 = springer, 2 = summer, 3 = fall, 4 = winter). Pada data ini season 1 mencakup Januari–Maret.

---

## 2. Business Questions

1. **Pola permintaan per jam:** Bagaimana pola rata-rata penyewaan sepeda per jam pada hari kerja dibandingkan akhir pekan/libur selama 2011–2012, dan pada jam berapa puncak permintaan terjadi?
2. **Pengaruh cuaca:** Seberapa besar perbedaan rata-rata penyewaan harian berdasarkan kondisi cuaca, dan faktor cuaca mana yang paling berkorelasi dengan permintaan selama 2011–2012?
3. **Segmen pengguna:** Bagaimana komposisi dan pola penyewaan pengguna casual versus registered berdasarkan musim dan tipe hari selama 2011–2012, dan segmen mana yang paling berpotensi ditingkatkan?

Ketiga pertanyaan dirumuskan dengan kerangka **SMART** (Specific, Measurable, Action-Oriented, Relevant, Time-bound). Penjelasan lengkap tersedia pada `notebook.ipynb`.

---

## 3. Struktur Proyek

```text
PROJECT Analisis Data Dicoding/
├── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv          # data per jam hasil cleaning
│   └── main_data_daily.csv    # data harian hasil cleaning
├── data/
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── notebook.ipynb             # notebook sudah dijalankan beserta output
├── README.md
├── requirements.txt
└── url.txt
```

---

## 4. Cara Menjalankan Dashboard

### Prasyarat

- Python 3.9 atau lebih baru
- pip

### Langkah umum

1. Ekstrak berkas ZIP submission (atau clone repositori jika tersedia).
2. Buka terminal dan masuk ke folder proyek.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan dashboard:

   ```bash
   streamlit run dashboard/dashboard.py
   ```

5. Buka `http://localhost:8501` pada browser.

### Windows (PowerShell)

```powershell
cd "PROJECT Analisis Data Dicoding"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

### macOS/Linux

```bash
cd "PROJECT Analisis Data Dicoding"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

### Jika data dashboard tidak ditemukan

Berkas `dashboard/main_data.csv` dan `dashboard/main_data_daily.csv` sudah disertakan. Jika ingin meregenerasi keduanya, buka `notebook.ipynb` dan jalankan seluruh cell dari awal. Notebook akan menyimpan ulang kedua berkas tersebut ke folder `dashboard/`.

---

## 5. Cara Menjalankan Notebook

Notebook sudah berisi output, tetapi dapat dijalankan ulang:

1. Buka folder proyek di VS Code, buka `notebook.ipynb`, lalu pilih kernel **Python 3 (ipykernel)**.
2. Atau jalankan JupyterLab dari terminal:

   ```bash
   jupyter lab
   ```

   lalu buka `notebook.ipynb`.
3. Pilih **Run All**. Notebook membaca `data/day.csv` dan `data/hour.csv`, lalu menulis ulang `dashboard/main_data.csv` dan `dashboard/main_data_daily.csv`.

Jika `jupyter` belum tersedia, install dengan `pip install jupyterlab notebook`.

---

## 6. Fitur Dashboard

- **Filter interaktif:** rentang tanggal, musim, tipe hari, dan kondisi cuaca.
- **KPI cards:** total penyewaan, rata-rata penyewaan harian, proporsi registered, dan proporsi casual.
- **Tab Ringkasan:** tren bulanan, tren harian dengan moving average 7 hari, total per musim, dan heatmap hari × jam.
- **Tab Pola Jam:** kurva permintaan per jam untuk hari kerja vs akhir pekan/libur, rata-rata per blok waktu, dan tabel jam tersibuk.
- **Tab Cuaca:** rata-rata penyewaan per kondisi cuaca, scatter suhu vs permintaan, dan korelasi faktor cuaca.
- **Tab Segmen Pengguna:** komposisi registered vs casual per musim, pola per jam per tipe pengguna, dan total per tahun.
- **Tab Segmentasi Permintaan:** profil segmen Low/Medium/High/Very High, jumlah hari per segmen, dan komposisi musim.
- **Tab Kesimpulan:** ringkasan temuan dan action item prioritas.

---

## 7. Insight Utama

- **Pola jam:** hari kerja memiliki pola bimodal dengan puncak pukul **08.00 (477 sepeda/jam)** dan **17.00 (525 sepeda/jam)**. Akhir pekan/libur memiliki satu puncak siang pukul **13.00 (373 sepeda/jam)**.
- **Cuaca:** dibanding cuaca cerah/berawan (4.877 penyewaan/hari), cuaca berkabut/mendung menurunkan permintaan **17,2%**, sedangkan hujan/salju ringan menurunkan **63,0%** menjadi 1.803 penyewaan/hari. Suhu berkorelasi positif kuat (**r ≈ 0,63**).
- **Segmen pengguna:** registered menyumbang **81,2%** penyewaan; casual **18,8%**. Proporsi casual lebih tinggi pada akhir pekan/libur (**31,7%**) dan musim Summer/Fall (sekitar **21–22%**).
- **Segmentasi permintaan:** segmen Very High memiliki rata-rata **7.042 penyewaan/hari** dan didominasi cuaca cerah, suhu hangat, serta musim Fall/Summer. Segmen Low rata-rata **1.934 penyewaan/hari** dan didominasi musim Spring.

---

## 8. Analisis Lanjutan

Teknik analisis lanjutan yang diterapkan adalah **clustering melalui binning kuartil** (tanpa machine learning). Data harian dibagi menjadi empat segmen berdasarkan `cnt`:

- **Low:** 22–3.141 penyewaan/hari
- **Medium:** 3.163–4.548
- **High:** 4.549–5.936
- **Very High:** 5.976–8.714

Setiap segmen diprofilkan berdasarkan suhu, kelembapan, kecepatan angin, tipe hari, musim, dan kondisi cuaca. Teknik ini relevan untuk perencanaan armada dan penjadwalan perawatan.

Selain itu, **manual grouping** digunakan untuk mengelompokkan jam menjadi blok waktu (malam, pagi, siang, sore, malam) pada analisis pola jam.

---

## 9. Prinsip Visualisasi yang Diterapkan

- Grafik batang dimulai dari nol agar tidak misleading.
- Warna digunakan secara konsisten dan ramah buta warna untuk membedakan kategori.
- Setiap grafik memiliki judul, label sumbu dengan satuan, anotasi nilai penting, dan catatan sumber.
- Tidak menggunakan grafik 3D atau elemen dekoratif yang tidak menambah informasi (menjaga data-ink ratio).
- Perbandingan menggunakan satuan dan proporsi yang benar (menjaga lie factor tetap 1).

---

## 10. Deployment ke Streamlit Community Cloud

1. Push folder proyek ini ke repositori GitHub.
2. Masuk ke [Streamlit Community Cloud](https://share.streamlit.io/) dengan akun GitHub.
3. Pilih **New app**, lalu pilih repositori, branch, dan main file: `dashboard/dashboard.py`.
4. Klik **Deploy** dan tunggu proses selesai.
5. Salin URL dashboard yang dihasilkan, lalu ganti isi `url.txt` dengan URL tersebut.

> Dashboard telah dideploy ke Streamlit Community Cloud: [Live Demo](https://abhiprayaa29-bike-sharing-dashboard-dashboarddashboard-j5y8xb.streamlit.app/). URL yang sama tersimpan di `url.txt`.

---

## 11. Catatan dan Keterbatasan

- Dataset tidak memiliki ID pelanggan dan koordinat stasiun, sehingga RFM analysis dan geospatial analysis tidak dapat dilakukan secara valid.
- Terdapat 165 timestamp per jam yang hilang, sebagian besar pada dini hari (03.00–04.00).
- Jumlah hari hujan/salju ringan hanya 21 hari, sehingga estimasi dampak cuaca ekstrem memiliki ketidakpastian tinggi.
- `workingday = 0` menggabungkan akhir pekan dan hari libur.
- Data tidak memuat harga, pendapatan, atau kapasitas armada aktual.

---

## 12. Referensi

- Fanaee-T, H., & Gama, J. (2013). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence, 2, 113–127.
- UCI Machine Learning Repository. *Bike Sharing Dataset*. https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
- Dicoding. *Belajar Analisis Data dengan Python* — materi Data Wrangling, EDA, Visualisasi Data, dan Dashboard.
