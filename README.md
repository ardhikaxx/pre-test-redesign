# PIECES Framework Analysis - SIM Online Polije

Proyek ini digunakan untuk menganalisis kepuasan pengguna Website SIM Online Polije menggunakan metode **PIECES Framework**. Analisis dilakukan pada data kuesioner yang dibagi menjadi dua kelompok: **Pre-test** dan **Post-test**.

## Struktur Proyek
- `data/`: Berisi file CSV hasil kuesioner (D3 dan D4).
- `output/`: Berisi hasil analisis dalam bentuk CSV dan grafik.
- `pieces_analysis.py`: Script utama untuk memproses data dan menghitung skor PIECES.

## Metodologi
Skor dihitung berdasarkan rata-rata dari 20 pertanyaan yang dipetakan ke dalam 6 kategori PIECES:
1. **PERFORMANCE** (Kinerja): Pertanyaan 1-7
2. **INFORMATION** (Informasi): Pertanyaan 8-11
3. **ECONOMY** (Ekonomi): Pertanyaan 12-13
4. **CONTROL** (Kontrol): Pertanyaan 14-15
5. **EFFICIENCY** (Efisiensi): Pertanyaan 16-17
6. **SERVICE** (Layanan): Pertanyaan 18-20

### Pengelompokan Data
- **Pre-test**:
  - D3: Semester 1-4
  - D4: Semester 1-6
- **Post-test**:
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
Hasil analisis akan disimpan di folder `output/` dalam bentuk:
- `pieces_comparison_results.csv`: Tabel perbandingan skor pre-test vs post-test.
- `pieces_comparison_chart.png`: Grafik batang perbandingan skor.
