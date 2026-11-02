# Panduan Menjalankan Praktikum Dasar XML-RPC

## Persyaratan
- Python 3.10 ke atas (pustaka `xmlrpc` sudah bawaan dari Python standard library).

## Langkah Menjalankan
1. Buka Terminal pertama untuk menjalankan Server:
   ```bash
   python server_kalkulator.py
   ```
   Pastikan muncul pesan: `Server XML-RPC berjalan di port 8000...`.

2. Buka Terminal kedua untuk menjalankan Client:
   ```bash
   python client_kalkulator.py
   ```

3. Client akan menampilkan daftar method yang didukung server, hasil kalkulasi aritmatika, serta pencetakan payload HTTP & XML mentah karena parameter `verbose=True` diaktifkan.
