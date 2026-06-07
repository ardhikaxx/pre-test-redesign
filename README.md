# PIECES Framework Analysis - SIM Online Polije (Pre-test)

Proyek ini digunakan untuk menganalisis kepuasan pengguna Website SIM Online Polije menggunakan metode **PIECES Framework** pada fase **Pre-test**. Analisis dilakukan dengan menggabungkan dua kelompok kuesioner untuk mendapatkan gambaran kepuasan yang komprehensif dari berbagai tingkatan semester.

## Struktur Proyek
- `data/`: Berisi file CSV mentah hasil kuesioner (D3 dan D4).
- `output/`: Berisi hasil analisis akhir:
  - `D3/`: Hasil total untuk program studi D3 (Gabungan K1 + K2).
  - `D4/`: Hasil total untuk program studi D4 (Gabungan K1 + K2).
  - `comparison_D3_vs_D4.png`: Grafik perbandingan kepuasan antara D3 dan D4.
- `pieces_analysis.py`: Script Python utama untuk pengolahan data, perhitungan skor, dan visualisasi.

## Metodologi
Skor dihitung berdasarkan rata-rata dari 20 pertanyaan yang dipetakan ke dalam 6 kategori PIECES:
1. **PERFORMANCE** (Kinerja): Pertanyaan 1-7
2. **INFORMATION** (Informasi): Pertanyaan 8-11
3. **ECONOMY** (Ekonomi): Pertanyaan 12-13
4. **CONTROL** (Kontrol): Pertanyaan 14-15
5. **EFFICIENCY** (Efisiensi): Pertanyaan 16-17
6. **SERVICE** (Layanan): Pertanyaan 18-20

### Pengelompokan Data (Pre-test)
Data diambil dari dua kuesioner yang kemudian digabungkan untuk masing-masing program:
- **Kuesioner 1**:
  - D3: Semester 1-4
  - D4: Semester 1-6
- **Kuesioner 2**:
  - D3: Semester 5-6
  - D4: Semester 7-8

## Cara Menjalankan
1. Pastikan library yang dibutuhkan sudah terinstall:
   ```bash
   pip install pandas matplotlib seaborn
   ```
2. Jalankan script analisis:
   ```bash
   python pieces_analysis.py
   ```

## Hasil Analisis
Setiap grafik yang dihasilkan telah dilengkapi dengan **indikator nilai** di atas batang grafik untuk memudahkan pembacaan data secara presisi. Ambang batas kepuasan ditetapkan pada skor **3.41**.
