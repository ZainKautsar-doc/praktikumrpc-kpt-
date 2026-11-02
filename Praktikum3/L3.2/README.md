# Panduan Menjalankan Latihan L3.2

## Deskripsi
Latihan L3.2 mendemonstrasikan kegagalan deduplikasi akibat bug implementasi client, di mana client secara keliru men-generate UUID baru pada setiap iterasi percobaan pengulangan (*retry*). Hal ini menyebabkan server mengeksekusi transfer berkali-kali untuk satu transaksi yang sama (*transfer ganda*).

## Cara Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Amati saldo akhir rekening A: Saldo A akan berkurang lebih dari 200 (misalnya menjadi 720, 680, dst.) dan saldo B bertambah lebih dari 200 karena transfer ganda saat timeout terjadi.
