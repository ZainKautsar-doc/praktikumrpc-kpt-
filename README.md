# Praktikum Komputasi Paralel dan Terdistribusi (KPT) - Remote Procedure Call (RPC)

Repositori ini berisi kumpulan tugas, implementasi kode sumber, latihan, dan pengujian untuk modul Remote Procedure Call (RPC) menggunakan protokol **XML-RPC** dan **gRPC (Protocol Buffers)**.

---

## Identitas Praktikan

- **Nama**: Zain Kautsar Ridha
- **NIM**: 247006111153
- **Kelas**: EF / F-153
- **Mata Kuliah**: Komputasi Paralel dan Terdistribusi

---

## Ringkasan Modul Praktikum

### 1. Praktikum 1: RPC Dasar dengan XML-RPC
Implementasi RPC berbasis teks XML di atas transport HTTP/1.1 menggunakan modul bawaan Python (`xmlrpc.server` dan `xmlrpc.client`).
- **Praktikum (Modul Utama)**: Operasi kalkulator dasar (`tambah`, `kali`, `bagi`) dengan penanganan error/fault.
- **L1.1**: Penambahan fungsi matematika tingkat lanjut (`pangkat`, `akar`).
- **L1.2**: Prosedur string manipulation (`reverse_text`, `hitung_karakter`, `kapitalisasi`).
- **L1.3**: Pemanfaatan `MultiCall` untuk batch execution request dalam satu koneksi HTTP.
- **L1.4**: Modifikasi `SimpleXMLRPCRequestHandler` untuk pembatasan whitelist IP client.
- **L1.5**: Sistem autentikasi sederhana berbasis token/API key pada header HTTP.

### 2. Praktikum 2: gRPC dan Protocol Buffers
Implementasi high-performance RPC berbasis binary serialization (Protocol Buffers) dan transport HTTP/2 menggunakan pustaka gRPC Python.
- **Praktikum (Modul Utama)**: Layanan akademik (`AmbilKHS`) dengan definisi proto, server implementation, dan client stub.
- **L2.1**: Penambahan RPC method baru `HitungIPK` pada interface service.
- **L2.2**: Definisi dan implementasi Server Streaming RPC (`StreamNilaiSemester`).
- **L2.3**: Studi kompatibilitas skema Protocol Buffers (penambahan backward-compatible field tanpa breaking changes).
- **L2.4**: Integrasi gRPC Interceptor di sisi server untuk logging latency dan metadata request.
- **L2.5**: Pemanggilan RPC asinkron (`grpc.aio`) di sisi client untuk operasi non-blocking.

### 3. Praktikum 3: Concurrency, Timeout, dan Toleransi Kegagalan
Pengujian performa, ketahanan jaringan, penanganan beban konkuren, serta high-availability pada arsitektur RPC.
- **Praktikum (Modul Utama)**: Baseline pengujian concurrent requests dan timeout control.
- **L3.1**: Analisis pengaruh `ThreadPoolExecutor(max_workers=...)` terhadap throughput server.
- **L3.2**: Pengaturan timeout deadline (`timeout=...`) dan penanganan `grpc.StatusCode.DEADLINE_EXCEEDED`.
- **L3.3**: Pola Client Retry dengan algoritma Exponential Backoff dan Jitter untuk request idempoten.
- **L3.4**: Script benchmarking perbandingan performa latensi dan overhead antara XML-RPC vs. gRPC.
- **L3.5**: Arsitektur High Availability (HA) dengan sistem failover otomatis dari Server Primer ke Server Sekunder.

---

## Struktur Direktori

```text
PraktikumRPC(KPT)/
├── README.md                      # Dokumentasi utama proyek
├── detail_soal.md                 # Panduan & pembahasan teknis lengkap
├── Latihan & Praktikum RPC.pdf    # Modul panduan praktikum
├── Latihan Soal Teori/            # Jawaban tugas & soal teori
├── Praktikum1/                    # Implementasi XML-RPC
│   ├── Praktikum/
│   ├── L1.1/ s.d. L1.5/
├── Praktikum2/                    # Implementasi gRPC & Protobuf
│   ├── Praktikum/
│   ├── L2.1/ s.d. L2.5/
└── Praktikum3/                    # Concurrency, Retry, & Failover
    ├── Praktikum/
    ├── L3.1/ s.d. L3.5/
```

---

## Prasyarat & Instalasi

### 1. Kebutuhan Lingkungan
- Python 3.8 atau lebih baru.
- Manajemen paket `pip`.

### 2. Instalasi Dependensi
Jalankan perintah berikut untuk menginstal pustaka yang dibutuhkan:
```bash
pip install grpcio grpcio-tools protobuf
```

### 3. Kompilasi Protocol Buffers (Jika Mengubah `.proto`)
Untuk mengompilasi file skema proto menjadi stub Python:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. <nama_file>.proto
```

---

## Cara Menjalankan

### Menjalankan XML-RPC (Praktikum 1)
1. Jalankan server:
   ```bash
   python Praktikum1/Praktikum/server_kalkulator.py
   ```
2. Jalankan client pada terminal terpisah:
   ```bash
   python Praktikum1/Praktikum/client_kalkulator.py
   ```

### Menjalankan gRPC (Praktikum 2 & 3)
1. Jalankan server:
   ```bash
   python Praktikum2/Praktikum/server_grpc.py
   ```
2. Jalankan client pada terminal terpisah:
   ```bash
   python Praktikum2/Praktikum/client_grpc.py
   ```

### Menjalankan Skenario Failover (Praktikum 3 - L3.5)
1. Jalankan server primer (port 50051) dan sekunder (port 50052):
   ```bash
   python Praktikum3/L3.5/server_primer.py
   python Praktikum3/L3.5/server_sekunder.py
   ```
2. Jalankan client failover:
   ```bash
   python Praktikum3/L3.5/client_failover.py
   ```
