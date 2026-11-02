# LAPORAN PRAKTIKUM 2 — LATIHAN L2.2

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 2 (Latihan L2.2 — Implementasi RPC Bidirectional Streaming)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mahasiswa memahami prinsip dan implementasi **Bidirectional Streaming** pada protokol gRPC.
2. Mahasiswa mampu merancang antarmuka pertukaran pesan dua arah (full duplex) untuk simulasi ruang diskusi atau pesan interaktif secara realtime.

### B. Dasar Teori Singkat
Bidirectional Streaming (dua arah) adalah tipe pemanggilan gRPC di mana client dan server membaca serta menulis urutan pesan secara independen menggunakan koneksi HTTP/2 multiplexing. Kedua belah pihak dapat mengirimkan pesan kapan saja dalam urutan bebas tanpa harus menunggu lawan bicaranya selesai (full-duplex). Pola ini sangat tepat digunakan untuk aplikasi chat real-time, game multiplayer, pemantauan telemetri IoT dua arah, dan sistem kontrol berbasis event.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Menambahkan definisi struktur data `Pesan` dan RPC `Diskusi` pada berkas `akademik.proto`:
   ```protobuf
   message Pesan {
     string pengirim = 1;
     string isi = 2;
     string waktu = 3;
   }
   rpc Diskusi (stream Pesan) returns (stream Pesan);
   ```
2. Mengompilasi berkas `.proto` menjadi stub Python.
3. Di sisi server, mengimplementasikan method `Diskusi` yang membaca iterasi pesan masuk dan memancarkan (`yield`) balasan instan.
4. Di sisi client, membuat generator pengirim pesan dan loop pembaca respons balasan.

### B. Kode Program
#### Server (`server.py`):
```python
import time
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.2 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def Diskusi(self, request_iterator, context):
        print("\n[SERVER DISKUSI] Sesi diskusi client terhubung!")
        for pesan_masuk in request_iterator:
            waktu_terima = time.strftime("%H:%M:%S")
            print(f"[{waktu_terima}] Pesan dari [{pesan_masuk.pengirim}]: {pesan_masuk.isi}")
            yield pb.Pesan(
                pengirim="Server Akademik Bot",
                isi=f"Halo {pesan_masuk.pengirim}, pesan Anda ('{pesan_masuk.isi}') telah diterima.",
                waktu=time.strftime("%H:%M:%S")
            )

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L2.2] Server Chat Diskusi gRPC berjalan di port 50051...")
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
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.2 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def generator_pesan_client():
    daftar_chat = [
        "Halo server, apakah nilai UTS Basis Data sudah final?",
        "Kapan jadwal perbaikan nilai mata kuliah Jaringan?",
        "Terima kasih atas konfirmasinya!"
    ]
    for chat in daftar_chat:
        pesan_obj = pb.Pesan(
            pengirim="Zain (NPM: 247006111153)",
            isi=chat,
            waktu=time.strftime("%H:%M:%S")
        )
        print(f"\n[CLIENT SEND ->] {pesan_obj.isi}")
        yield pesan_obj
        time.sleep(1.0)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        stream_respons = stub.Diskusi(generator_pesan_client())
        for balasan in stream_respons:
            print(f"[CLIENT RECV <-] Dari: {balasan.pengirim} | Jam: {balasan.waktu}")
            print(f"                 Pesan: {balasan.isi}")

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), inisialisasi sesi diskusi, serta log penerimaan pesan teks dari client secara realtime beserta timestamp.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, urutan transmisi pesan client (`[CLIENT SEND ->]`), dan balasan otomatis seketika dari bot server (`[CLIENT RECV <-]`) yang saling berselingan tanpa jeda pemutusan koneksi.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Keunggulan HTTP/2 Multiplexing
Pada arsitektur Web tradisional (HTTP/1.1), komunikasi dua arah umumnya memerlukan polling berkala (long-polling) atau pembukaan koneksi WebSocket tambahan. Pada gRPC, bidirectional streaming berjalan secara native di atas lapisan HTTP/2:
1. Satu koneksi TCP fisik dapat mengalirkan frame data client-to-server dan frame data server-to-client secara bersamaan tanpa saling memblokir (tidak ada *head-of-line blocking* di tingkat protokol HTTP).
2. Setiap pesan di-serialize menggunakan Protocol Buffers biner yang hemat bandwidth dan meminimalkan latensi overhead komunikasi.

### B. Prompt AI untuk Men-generate Diagram Bidirectional Streaming
Gunakan prompt berikut pada AI generator untuk membuat visualisasi interaksi dua arah:
> *"Create a professional full-duplex communication architectural diagram representing gRPC Bidirectional Streaming. In the center, show a bidirectional HTTP/2 pipe with two parallel data lanes: top lane in emerald green flowing right with 'Client Message Stream', and bottom lane in bright cyan flowing left with 'Server Response Stream'. On the left, display a 'Client Terminal' and on the right a 'gRPC Server Node'. Sleek futuristic dark theme, high resolution, precise network flow arrows, clean sans-serif annotations."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Bidirectional streaming gRPC memungkinkan percakapan interaktif dua arah yang sangat responsif dengan utilisasi sumber daya jaringan yang minimal.
2. Penanganan stream di kedua sisi dapat dieksekusi secara asinkron atau terpisah pada thread berbeda untuk throughput maksimal.

### B. Kendala yang Dihadapi
Jika client membaca stream balasan secara serial pada thread yang sama dengan generator, client baru dapat membaca tanggapan setelah buffer transmisi selesai atau terjadi pergantian konteks eksekusi I/O.
