# Panduan Menjalankan Latihan L1.2

## Deskripsi
Latihan L1.2 mengimplementasikan prosedur remote `statistik(daftar)` yang menerima list nilai angka dan mengembalikan dictionary hasil agregasi (`min`, `max`, `rata2`). Mode `verbose=True` diaktifkan di client untuk mengamati proses marshalling tipe data koleksi menjadi tag `<array>` dan `<struct>` pada XML.

## Cara Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Amati pada layar client struktur XML yang dikirimkan melalui HTTP POST (`<array>`) serta struktur XML yang diterima kembali (`<struct>`).
