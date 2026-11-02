# Panduan Menjalankan Latihan L3.1

## Deskripsi
Latihan L3.1 membuktikan semantik **At-Most-Once** pada gRPC melalui mekanisme deduplikasi `request_id` unik. Meskipun server mengalami timeout buatan 3 detik (melebihi batas timeout client 2.0 detik) dan client mengirim ulang request, transaksi hanya dieksekusi satu kali sehingga total saldo sistem tetap utuh 1500.

## Cara Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Amati log konsol saat terjadi timeout dan retry. Pada akhir eksekusi 20 transaksi nominal 10, pastikan Saldo A bernilai 800 dan Saldo B bernilai 700.
