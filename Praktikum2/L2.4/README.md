# Panduan Menjalankan Latihan L2.4

## Deskripsi
Latihan L2.4 membandingkan ukuran byte serialisasi antara representasi biner Protocol Buffers (`len(mhs.SerializeToString())`) dengan representasi teks XML-RPC untuk objek data mahasiswa yang identik.

## Cara Menjalankan
1. Pastikan stub `akademik_pb2.py` sudah di-generate di folder `Praktikum2/Praktikum`.
2. Jalankan skrip analisis:
   ```bash
   python compare_payload.py
   ```
3. Skrip akan mencetak representasi heksadesimal biner Protobuf, string XML mentah, ukuran dalam bytes, rasio perbandingan, serta persentase penghematan bandwidth.
