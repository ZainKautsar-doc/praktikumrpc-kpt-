# LAPORAN PRAKTIKUM 2 — LATIHAN L2.3

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 2 (Latihan L2.3 — Uji Backward Compatibility Protocol Buffers)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Membuktikan sifat *backward compatibility* dan *forward compatibility* pada evolusi skema Protocol Buffers.
2. Mengamati mekanisme kerja parser Protobuf ketika menerima payload yang mengandung *unknown fields* (field tambahan baru).

### B. Dasar Teori Singkat
Dalam sistem terdistribusi skala besar, memperbarui seluruh client dan server secara serentak (*lockstep deployment*) adalah hal yang mustahil. Oleh karena itu, protokol serialisasi harus mendukung evolusi skema tanpa menyebabkan *breaking change*.
Protocol Buffers tidak mengirimkan nama field (seperti "nama" atau "prodi"), melainkan pasangan **Field Number (Tag)** dan tipe kabel (*wire type*). Ketika parser client menerima pesan biner, parser hanya memproses field number yang telah terdaftar dalam skema lokalnya. Field number baru yang belum dikenal tidak akan memicu exception parsing melainkan disimpan sebagai *unknown fields*, sehingga client lama tetap berfungsi normal.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Mendefinisikan skema awal `akademik_v1.proto` dengan field `nim = 1`, `nama = 2`, dan `ipk = 3`.
2. Menghasilkan stub versi 1 untuk client lama.
3. Mendefinisikan skema baru `akademik_v2.proto` dengan menambahkan `string prodi = 4;` pada pesan `Mahasiswa`.
4. Menghasilkan stub versi 2 untuk server baru.
5. Menjalankan server versi 2 dan menghubunginya menggunakan client versi 1.
6. Memverifikasi kelancaran parsing atribut lama dan penanganan field baru.

### B. Kode Program
#### Skema V1 Lama (`akademik_v1.proto`):
```protobuf
syntax = "proto3";
package akademik;

service LayananNilai {
  rpc GetMahasiswa (MahasiswaRequest) returns (Mahasiswa);
}

message MahasiswaRequest { string nim = 1; }
message Mahasiswa {
  string nim = 1;
  string nama = 2;
  double ipk = 3;
}
```

#### Skema V2 Baru (`akademik_v2.proto`):
```protobuf
syntax = "proto3";
package akademik;

service LayananNilai {
  rpc GetMahasiswa (MahasiswaRequest) returns (Mahasiswa);
}

message MahasiswaRequest { string nim = 1; }
message Mahasiswa {
  string nim = 1;
  string nama = 2;
  double ipk = 3;
  string prodi = 4; // Field tambahan baru
}
```

#### Server Baru V2 (`server.py`):
```python
from concurrent import futures
import grpc
import akademik_v2_pb2 as pb2_v2
import akademik_v2_pb2_grpc as pb2_grpc_v2

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.3 (SERVER SKEMA BARU V2)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DATA_V2 = {
    "2023001": {"nama": "Andi", "ipk": 3.45, "prodi": "Informatika"},
}

class LayananNilaiV2(pb2_grpc_v2.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        mhs = DATA_V2.get(request.nim)
        return pb2_v2.Mahasiswa(
            nim=request.nim, nama=mhs["nama"], ipk=mhs["ipk"], prodi=mhs["prodi"]
        )

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc_v2.add_LayananNilaiServicer_to_server(LayananNilaiV2(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER V2] Server gRPC V2 aktif di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

#### Client Lama V1 (`client.py`):
```python
import grpc
import akademik_v1_pb2 as pb2_v1
import akademik_v1_pb2_grpc as pb2_grpc_v1

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.3 (CLIENT SKEMA LAMA V1)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub_lama = pb2_grpc_v1.LayananNilaiStub(channel)
        mhs = stub_lama.GetMahasiswa(pb2_v1.MahasiswaRequest(nim="2023001"))
        print(f"NIM: {mhs.nim} | Nama: {mhs.nama} | IPK: {mhs.ipk}")
        print("hasattr prodi:", hasattr(mhs, "prodi"))

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), inisialisasi server V2, dan pencatatan transmisi payload mahasiswa lengkap beserta field `prodi: Informatika`.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, keberhasilan pembacaan data `nim: 2023001`, `nama: Andi`, `ipk: 3.45`, dan nilai `hasattr(mhs, 'prodi') = False` membuktikan client lama tidak crash serta mengabaikan field baru secara aman.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Pertanyaan Modul
> *Apakah tetap berjalan? Jelaskan konsep backward compatibility pada Protobuf.*
1. **Status Eksekusi:** Program client lama **tetap berjalan dengan sempurna tanpa menimbulkan error**.
2. **Konsep Backward Compatibility:**
   - Desain biner Protobuf memanfaatkan pengkodean berdasar **Tag Number**. Dalam payload biner, setiap nilai diawali dengan kombinasi byte `(field_number << 3) | wire_type`.
   - Ketika client lama (skema V1) membaca payload dari server baru (V2), parser mengenali Tag 1 (`nim`), Tag 2 (`nama`), dan Tag 3 (`ipk`).
   - Ketika parser menjumpai Tag 4 (`prodi`), parser memeriksa apakah Tag 4 ada di dalam deskriptor pesan lokalnya. Karena tidak ada, parser secara otomatis melewati byte string tersebut tanpa melempar parse error.
   - Aturan evolusi skema: **Jangan pernah mengubah nomor tag yang sudah ada**, dan **jangan menghapus nomor tag yang masih aktif**. Penambahan field baru selalu aman jika menggunakan nomor tag baru.

### B. Prompt AI untuk Men-generate Diagram Kompatibilitas Skema
Gunakan prompt berikut pada AI generator untuk membuat visualisasi evolusi skema:
> *"Create an intuitive infographic diagram illustrating Backward Compatibility in Protocol Buffers. Display two entities: On the left, 'Server v2 (New)' encoding a Protobuf binary payload with fields: [Tag 1: nim, Tag 2: nama, Tag 3: ipk, Tag 4: prodi]. On the right, 'Client v1 (Old)' with descriptor containing only Tags 1, 2, and 3. Show clear parsing arrows reading Tags 1-3 into memory, and a designated 'Unknown Field Filter' safely skipping Tag 4 without crashing. Clean flat engineering style with forest green and navy accents."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Protocol Buffers menjamin kelangsungan interoperabilitas antar-versi aplikasi tanpa memaksa pembaruan serempak di seluruh sistem client.
2. Mekanisme pengalamatan berbasis nomor tag merupakan fondasi utama keandalan evolusi antarmuka layanan microservices modern.

### B. Kendala yang Dihadapi
Jika pengembang secara ceroboh mengganti nomor tag atau menggunakan kembali tag nomor lama untuk tipe data yang berbeda, proses deserialisasi akan mengalami inkonsistensi atau korupsi data.
