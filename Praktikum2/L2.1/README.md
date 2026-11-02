# Panduan Menjalankan Latihan L2.1

## Deskripsi
Latihan L2.1 mengimplementasikan pola **Client Streaming** pada gRPC melalui RPC `KirimBanyakNilai(stream NilaiRequest) returns (StatusResponse)`. Client mengirim beberapa record nilai secara bertahap dalam satu stream, dan server mengembalikan ringkasan status tunggal.

## Cara Menjalankan
1. **Generate Stub (jika file .proto diubah):**
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. akademik.proto
   ```
2. **Jalankan Server:**
   ```bash
   python server.py
   ```
3. **Jalankan Client:**
   ```bash
   python client.py
   ```
4. Amati pengiriman tiap data dari generator client dan respons balasan dari server berupa jumlah data yang tersimpan.
