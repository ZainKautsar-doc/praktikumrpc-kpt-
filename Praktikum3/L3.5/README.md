# Panduan Menjalankan Latihan L3.5

## Deskripsi
Latihan L3.5 mengimplementasikan pengayaan sistem berupa arsitektur **Failover Otomatis** pada client gRPC menggunakan dua node server independen:
- Server Primer pada port `50051`
- Server Sekunder pada port `50052`

## Cara Menjalankan
1. **Terminal 1 — Jalankan Server Primer:**
   ```bash
   python server_primer.py
   ```
2. **Terminal 2 — Jalankan Server Sekunder:**
   ```bash
   python server_sekunder.py
   ```
3. **Terminal 3 — Jalankan Client Failover:**
   ```bash
   python client_failover.py
   ```
   Client akan terhubung ke port `50051` dan menampilkan pesan dari Server Primer.
4. **Simulasi Crash:**
   Pada Terminal 1 (Server Primer), tekan `Ctrl + C` untuk mematikan server.
5. **Amati Perpindahan Otomatis:**
   Client langsung mendeteksi status `UNAVAILABLE` pada port 50051 dan secara transparan mengalihkan permintaan berikutnya ke Server Sekunder port `50052` tanpa force close.
