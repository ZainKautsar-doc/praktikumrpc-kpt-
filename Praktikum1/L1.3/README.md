# Panduan Menjalankan Latihan L1.3

## Deskripsi
Latihan L1.3 menguji batas kemampuan transmisi tipe data bawaan XML-RPC terhadap dua kasus ekstrem: objek waktu (`datetime`) dan integer besar melampaui $2^{31}-1$.

## Cara Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Amati pesan `TypeError` pada transmisi `datetime` default dan `OverflowError` saat mengirimkan integer $> 2.147.483.647$, serta bagaimana alternatif solusinya bekerja.
