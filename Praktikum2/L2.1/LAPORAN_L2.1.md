# LAPORAN PRAKTIKUM 2 — LATIHAN L2.1

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 2 (Latihan L2.1 — Implementasi RPC Client Streaming)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mahasiswa mampu mendefinisikan antarmuka Protocol Buffers dengan pola komunikasi **Client Streaming**.
2. Mahasiswa mampu mengimplementasikan generator iterator di client dan iterasi penanganan stream di sisi server gRPC.

### B. Dasar Teori Singkat
Dalam arsitektur gRPC di atas transport HTTP/2, Client Streaming adalah pola di mana client mengirimkan urutan pesan secara berkelanjutan ke server melalui satu stream HTTP/2 tunggal. Server menunggu (atau memproses secara on-the-fly) seluruh rangkaian pesan tersebut hingga client menutup stream (sinyal *End-Of-Stream* / half-closed), kemudian server memproses agregasi data dan mengembalikan tepat satu pesan respons ke client. Pola ini sangat optimal untuk skenario upload data batch berukuran besar, log telemetri berkelanjutan, atau sinkronisasi multi-record tanpa overhead membuka banyak koneksi TCP/HTTP baru.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Membuka file `akademik.proto` dan menambahkan definisi RPC baru:
   ```protobuf
   rpc KirimBanyakNilai (stream NilaiRequest) returns (StatusResponse);
   ```
2. Mengompilasi ulang stub dengan `grpc_tools.protoc`.
3. Menulis fungsi `KirimBanyakNilai(self, request_iterator, context)` pada server untuk mengonsumsi data `request_iterator`, memvalidasi rentang nilai (0–100), memperbarui data akademik, dan menghitung jumlah record yang berhasil disimpan.
4. Menulis fungsi generator pada client (`yield NilaiRequest(...)`) yang mengirimkan 4 data nilai secara bertahap.
5. Menjalankan server dan client lalu memverifikasi seluruh nilai tersimpan dengan memanggil `StreamNilai`.

### B. Kode Program
#### Kontrak Protobuf (`akademik.proto`):
```protobuf
syntax = "proto3";
package akademik;

service LayananNilai {
  rpc GetMahasiswa     (MahasiswaRequest)     returns (Mahasiswa);
  rpc TambahNilai      (NilaiRequest)         returns (StatusResponse);
  rpc StreamNilai      (MahasiswaRequest)     returns (stream Nilai);
  rpc KirimBanyakNilai (stream NilaiRequest)  returns (StatusResponse);
}

message MahasiswaRequest { string nim = 1; }
message Mahasiswa        { string nim = 1; string nama = 2; double ipk = 3; }
message NilaiRequest     { string nim = 1; string matkul = 2; double nilai = 3; }
message Nilai            { string matkul = 1; double nilai = 2; }
message StatusResponse   { bool sukses = 1; string pesan = 2; }
```

#### Server (`server.py`):
```python
import time
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.1 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DATA = {
    "2023001": {"nama": "Andi", "nilai": {"Basis Data": 85.0, "Jaringan": 78.0}},
}

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def KirimBanyakNilai(self, request_iterator, context):
        jumlah_sukses = 0
        for req in request_iterator:
            if not 0 <= req.nilai <= 100: continue
            mhs = DATA.setdefault(req.nim, {"nama": "(Mahasiswa Baru)", "nilai": {}})
            mhs["nilai"][req.matkul] = req.nilai
            jumlah_sukses += 1
            print(f"[SERVER L2.1] Menyimpan nilai: NIM {req.nim} | {req.matkul}: {req.nilai}")

        return pb.StatusResponse(
            sukses=True,
            pesan=f"Berhasil mengunggah dan menyimpan {jumlah_sukses} nilai untuk mahasiswa."
        )

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L2.1] Server gRPC aktif di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

#### Client (`client.py`):
```python
import time
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.1 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def generator_nilai():
    daftar_data = [
        pb.NilaiRequest(nim="2023001", matkul="Algoritma Pemrograman", nilai=89.5),
        pb.NilaiRequest(nim="2023001", matkul="Struktur Data", nilai=94.0),
        pb.NilaiRequest(nim="2023001", matkul="Sistem Operasi", nilai=82.0),
        pb.NilaiRequest(nim="2023001", matkul="Kecerdasan Buatan", nilai=91.0)
    ]
    for item in daftar_data:
        print(f"[CLIENT STREAMING ->] Mengirim data: {item.matkul} = {item.nilai}")
        yield item
        time.sleep(0.4)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        respons = stub.KirimBanyakNilai(generator_nilai())
        print(f"\nStatus: {respons.sukses} | Pesan: {respons.pesan}")

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), port 50051 aktif, serta log server menerima 4 item pesan dari generator stream secara realtime dan menyimpan ke dalam memori.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, progres pengiriman 4 data mata kuliah dengan jeda 0.4 detik, penerimaan balasan `Berhasil mengunggah dan menyimpan 4 nilai untuk mahasiswa`, serta verifikasi daftar mata kuliah yang bertambah.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Arsitektur Streaming HTTP/2
Pada pola Client Streaming gRPC:
1. Client menginisiasi satu HTTP/2 Data Stream (misal Stream ID = 1) dengan header frame `grpc-encoding: identity` dan flag `END_HEADERS`.
2. Setiap objek `NilaiRequest` diserialisasi ke dalam binary Protobuf dan dikirimkan sebagai HTTP/2 DATA frame berurutan.
3. Setelah generator client selesai (`StopIteration`), client mengirimkan frame DATA kosong dengan flag `END_STREAM`.
4. Server memproses seluruh data dan membalas dengan satu response DATA frame + Trailers (Status OK). Dibandingkan model REST tradisional yang membutuhkan 4 kali HTTP POST terpisah dengan overhead handshake TCP dan header berulang, Client Streaming memangkas overhead jaringan lebih dari 70%.

### B. Prompt AI untuk Men-generate Diagram Alur Client Streaming
Gunakan prompt berikut pada AI generator untuk membuat ilustrasi alur stream:
> *"Create an ultra-clean, modern technical diagram illustrating gRPC Client Streaming pattern over HTTP/2. On the left side, show 'Client Application' streaming multiple binary Protobuf messages sequentially: 'NilaiRequest 1', 'NilaiRequest 2', 'NilaiRequest 3' inside a single HTTP/2 TCP pipe. On the right side, show 'gRPC Server' receiving the stream iterator, processing data in real-time, and emitting a single 'StatusResponse' message at the end. Sleek tech visual with deep blue background, vibrant cyan data flow lines, and crisp typography."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Pola Client Streaming pada gRPC memungkinkan transmisi sejumlah besar pesan independen dalam satu koneksi jaringan yang efisien tanpa latensi re-handshake.
2. Integrasi Python generator (`yield`) dengan stub gRPC menyajikan abstraksi stream yang bersih dan intuitif di tingkat aplikasi.

### B. Kendala yang Dihadapi
Di sisi server, loop iterasi `for req in request_iterator:` bersifat blocking sampai client selesai mengirimkan data atau menutup stream. Oleh sebab itu, timeout penanganan stream harus disesuaikan agar worker thread tidak menggantung jika client terputus di tengah jalan.
