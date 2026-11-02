# Panduan Menjalankan Latihan L1.1

## Deskripsi
Latihan L1.1 menambahkan implementasi fungsi matematika `pangkat(a, b)` dan `akar(x)` di sisi server XML-RPC dan mengujinya melalui remote call dari sisi client.

## Cara Menjalankan
1. **Jalankan Server:**
   Buka terminal di folder `Praktikum1/L1.1` dan jalankan:
   ```bash
   python server.py
   ```

2. **Jalankan Client:**
   Buka terminal kedua di folder `Praktikum1/L1.1` dan jalankan:
   ```bash
   python client.py
   ```

3. Amati output identitas mahasiswa serta hasil pemanggilan fungsi `pangkat` dan `akar` beserta validasi error bilangan negatif.
