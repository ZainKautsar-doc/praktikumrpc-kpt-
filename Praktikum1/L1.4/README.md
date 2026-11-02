# Panduan Menjalankan Latihan L1.4

## Deskripsi
Latihan L1.4 melakukan benchmarking kinerja antara 100 kali pemanggilan fungsi lokal murni versus 100 kali pemanggilan fungsi remote melalui XML-RPC menggunakan presisi tinggi `time.perf_counter()`.

## Cara Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Terminal client akan mencetak tabel perbandingan waktu total eksekusi dan latensi rata-rata per panggilan dalam milidetik.
