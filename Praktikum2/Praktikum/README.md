# Panduan Menjalankan Praktikum Dasar gRPC

## Persyaratan
- Python 3.10 ke atas
- Pustaka `grpcio` dan `grpcio-tools` (terpasang via `pip install grpcio grpcio-tools`)

## Langkah Menjalankan
1. **Generate Stub Protobuf (Jika belum dibuat):**
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. akademik.proto
   ```
   Perintah ini akan menghasilkan `akademik_pb2.py` dan `akademik_pb2_grpc.py`.

2. **Jalankan Server gRPC:**
   Buka terminal pertama di direktori ini:
   ```bash
   python server_grpc.py
   ```
   Server akan berjalan dan mendengarkan pada port `50051`.

3. **Jalankan Client gRPC:**
   Buka terminal kedua di direktori ini:
   ```bash
   python client_grpc.py
   ```
   Client akan mendemonstrasikan pemanggilan Unary `GetMahasiswa`, `TambahNilai`, serta Server Streaming `StreamNilai`.
