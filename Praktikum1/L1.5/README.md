# Panduan Menjalankan Latihan L1.5

## Deskripsi
Latihan L1.5 mensimulasikan kegagalan sistem (server crash/mati) saat client sedang aktif berkomunikasi, mengamati tipe exception yang terlempar di lapisan socket/HTTP, dan menerapkan penanganan error terstruktur.

## Cara Menjalankan
1. **Jalankan Server:**
   Buka terminal pertama di folder `Praktikum1/L1.5`:
   ```bash
   python server.py
   ```

2. **Jalankan Client:**
   Buka terminal kedua di folder `Praktikum1/L1.5`:
   ```bash
   python client.py
   ```
   Client akan mulai mengirimkan permintaan setiap 2 detik.

3. **Simulasikan Crash Server:**
   Kembali ke terminal server, lalu tekan `Ctrl + C` untuk menghentikan server secara tiba-tiba.

4. **Amati Respon Client:**
   Client tidak akan mengalami crash tanpa kontrol, melainkan menangkap `ConnectionRefusedError` dan menampilkan pesan penanganan kegagalan yang ramah.
