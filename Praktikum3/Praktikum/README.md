# Panduan Menjalankan Praktikum 3 Dasar

## Persyaratan
- Python 3.10+
- `grpcio` dan `grpcio-tools`

## Langkah Menjalankan
1. **Jalankan Server:**
   ```bash
   python server.py
   ```
2. **Jalankan Client:**
   ```bash
   python client.py
   ```
3. Amati penanganan timeout 2.0s dengan mekanisme retry backoff (jeda 0.5s, 1.0s, dst.) serta deduplikasi Request ID di sisi server.
