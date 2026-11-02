# Panduan Menjalankan Latihan L3.4

## Deskripsi
Latihan L3.4 mengukur pengaruh jumlah worker threads server (`max_workers = 1, 4, 10`) terhadap throughput (permintaan per detik) dan latensi rata-rata pada 200 pemanggilan konkurensi tinggi dari 20 client threads.

## Cara Menjalankan Benchmark

### 1. Pengujian untuk max_workers = 1
1. Terminal 1: Jalankan server dengan 1 worker:
   ```bash
   python server.py 1
   ```
2. Terminal 2: Jalankan client benchmark:
   ```bash
   python client_benchmark.py
   ```
3. Catat Waktu Total, Throughput, dan Latensi Rata-rata. Hentikan server (Ctrl+C).

### 2. Pengujian untuk max_workers = 4
1. Terminal 1: Jalankan server dengan 4 workers:
   ```bash
   python server.py 4
   ```
2. Terminal 2: Jalankan client benchmark kembali:
   ```bash
   python client_benchmark.py
   ```
3. Catat hasilnya. Hentikan server.

### 3. Pengujian untuk max_workers = 10
1. Terminal 1: Jalankan server dengan 10 workers:
   ```bash
   python server.py 10
   ```
2. Terminal 2: Jalankan client benchmark kembali:
   ```bash
   python client_benchmark.py
   ```
3. Catat hasilnya dan bandingkan dalam tabel laporan.
