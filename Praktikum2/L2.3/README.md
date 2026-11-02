# Panduan Menjalankan Latihan L2.3

## Deskripsi
Latihan L2.3 membuktikan prinsip **Backward Compatibility** pada Protocol Buffers dengan menguji client lama (hanya mengenal nim, nama, ipk) terhadap server baru yang telah diperbarui dengan field tambahan `string prodi = 4;`.

## Cara Menjalankan
1. **Jalankan Server Versi Baru (V2):**
   ```bash
   python server.py
   ```
2. **Jalankan Client Versi Lama (V1):**
   ```bash
   python client.py
   ```
3. Amati bahwa client lama tetap dapat membaca pesan dari server baru secara normal tanpa mengalami exception parsing.
