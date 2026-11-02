# Panduan Menjalankan Latihan L2.2

## Deskripsi
Latihan L2.2 mengimplementasikan pola **Bidirectional Streaming** (aliran dua arah) pada gRPC melalui RPC `Diskusi(stream Pesan) returns (stream Pesan)`. Client dan server saling bertukar pesan percakapan secara asinkron dan realtime melalui satu koneksi HTTP/2 multiplexing.

## Cara Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Amati pertukaran pesan secara interaktif: client mengirim pesan teks secara bertahap dan server merespons balik setiap pesan tersebut secara realtime.
