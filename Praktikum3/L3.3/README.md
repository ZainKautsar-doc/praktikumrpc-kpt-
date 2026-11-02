# Panduan Menjalankan Latihan L3.3

## Deskripsi
Latihan L3.3 menguji konsekuensi penghapusan sinkronisasi thread (`with LOCK:`) di server ketika menerima beban konkurensi tinggi (50 transfer simultan dari 10 client threads), yang memicu terjadinya **Race Condition** dan **Lost Update**.

## Cara Menjalankan
1. **Jalankan Server Tanpa Lock:**
   ```bash
   python server.py
   ```
2. **Jalankan Client Uji Konkurensi:**
   ```bash
   python client.py
   ```
3. Periksa output saldo akhir di terminal: Total saldo rekening A dan B tidak lagi bernilai 1500 (uang hilang atau bertambah secara tidak valid).
