# Panduan Menjalankan Latihan L2.5

## Deskripsi
Latihan L2.5 mengubah mekanisme pemanggilan prosedur gRPC menjadi asinkron (non-blocking) menggunakan method `stub.GetMahasiswa.future(...)`. Client meluncurkan 10 request secara bersamaan tanpa menunggu antrean blocking dan memanen hasilnya secara paralel dengan `.result()`.

## Cara Menjalankan
1. **Jalankan Server:**
   Buka terminal pertama di folder `Praktikum2/L2.5`:
   ```bash
   python server.py
   ```
2. **Jalankan Client Asinkron:**
   Buka terminal kedua di folder `Praktikum2/L2.5`:
   ```bash
   python client_async.py
   ```
3. Amati bahwa seluruh 10 request dikirim dalam orde sub-milidetik, dan total waktu penyelesaian hampir identik dengan durasi 1 panggilan saja (~0.2 detik alih-alih 2.0 detik serial) karena diproses secara paralel oleh thread pool server.
