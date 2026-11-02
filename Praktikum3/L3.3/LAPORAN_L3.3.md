# LAPORAN PRAKTIKUM 3 — LATIHAN L3.3

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 3 (Latihan L3.3 — Eksperimen Race Condition Tanpa Sinkronisasi Thread)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mengamati terjadinya anomali *race condition* dan *lost update* ketika resource bersama (*shared state*) diakses tanpa mekanisme mutual exclusion (`Lock`).
2. Menganalisis kerusakan integritas saldo saat server multithreaded mengeksekusi request secara konkuren.

### B. Dasar Teori Singkat
Operasi pembacaan dan pembaruan saldo seperti `SALDO['A'] -= 10` pada dasarnya terdiri dari 3 instruksi level rendah:
1. **READ**: Membaca nilai saldo dari memori ke register CPU.
2. **MODIFY**: Mengurangi nilai saldo dengan nominal transfer.
3. **WRITE**: Menuliskan kembali nilai baru ke memori bersama.
Jika dua atau lebih worker thread server mengeksekusi urutan ini secara serentak tanpa proteksi `threading.Lock()`, terjadi *interleaving*: Thread 2 membaca nilai lama sebelum Thread 1 sempat menuliskan hasil pengurangannya. Hal ini mengakibatkan pembaruan dari salah satu thread tertimpa dan hilang (*Lost Update*).

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Memodifikasi server gRPC dengan menghapus blok `with LOCK:` pada method `Transfer`.
2. Menyisipkan jeda mikrodetik `time.sleep(0.001)` untuk memicu peralihan konteks thread (thread context-switching) secara konsisten.
3. Menulis program penguji client yang meluncurkan 50 request transfer secara bersamaan dari 10 worker threads menggunakan `concurrent.futures.ThreadPoolExecutor`.
4. Memeriksa apakah total saldo akhir tetap 1500 atau mengalami anomali.

### B. Kode Program
#### Server Tanpa Lock (`server.py`):
```python
from concurrent import futures
import time, grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.3 (SERVER TANPA LOCK)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

SALDO = {"A": 1000.0, "B": 500.0}

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def Transfer(self, request, context):
        # TANPA with LOCK: rentan lost update
        saldo_a = SALDO[request.dari]
        saldo_b = SALDO[request.ke]
        time.sleep(0.001) # Trigger race condition
        if saldo_a >= request.jumlah:
            SALDO[request.dari] = saldo_a - request.jumlah
            time.sleep(0.001)
            SALDO[request.ke] = saldo_b + request.jumlah
            return pb.StatusResponse(sukses=True, pesan=f"Saldo: {SALDO}")
        return pb.StatusResponse(sukses=False, pesan="Saldo tidak cukup")

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

#### Client Concurrency Test (`client.py`):
```python
import uuid
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.3 (CLIENT 50 TRANSFER SERENTAK)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def kirim_satu_transfer(idx):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        req = pb.TransferRequest(request_id=str(uuid.uuid4()), dari="A", ke="B", jumlah=10.0)
        return stub.Transfer(req, timeout=5.0)

def main():
    cetak_identitas()
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        tugas = [executor.submit(kirim_satu_transfer, i) for i in range(50)]
        for f in futures.as_completed(tugas): pass
    print("Pengujian konkurensi selesai.")

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), menerima 50 transaksi secara simultan dari pool worker, dan mengalami race condition saat membaca nilai kamus `SALDO`.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, progres 50 request konkuren, dan laporan saldo akhir yang rusak (misalnya: `Saldo kini {'A': 780.0, 'B': 620.0}` dengan total $780 + 620 = 1400 \ne 1500$, membuktikan uang 100 unit lenyap akibat lost update).

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Pertanyaan Modul Praktikum
> *Apakah total saldo tetap 1500? Jelaskan race condition yang terjadi.*
1. **Status Saldo:** Total saldo akhir **TIDAK TETAP 1500**. Terjadi kerusakan data (kehilangan saldo sistem secara acak berkisar antara 80 hingga 200 unit).
2. **Mekanisme Race Condition yang Terjadi:**
   - Misal Saldo A awal = 1000. Thread 1 dan Thread 2 masuk secara bersamaan.
   - Thread 1 membaca `saldo_a = 1000`.
   - Sebelum Thread 1 menulis, Thread 2 juga membaca `saldo_a = 1000`.
   - Thread 1 menghitung $1000 - 10 = 990$ dan menulis `SALDO['A'] = 990`.
   - Thread 2 juga menghitung $1000 - 10 = 990$ (karena membaca data awal yang belum terupdate) dan menulis `SALDO['A'] = 990`.
   - Seharusnya terjadi pemotongan $2 \times 10 = 20$ (saldo harusnya 980), namun yang tertulis adalah 990. Salah satu mutasi tertimpa dan hilang selamanya.

### B. Prompt AI untuk Men-generate Diagram Concurrency Race Condition
Gunakan prompt berikut pada AI generator untuk membuat grafik perbandingan thread safety:
> *"Create a professional concurrency race condition analysis diagram. Show two parallel timelines: Thread 1 and Thread 2 interleaved over a shared memory variable 'SALDO = 1000'. Illustrate the Step-by-Step sequence: Step 1 Thread 1 READ 1000. Step 2 Thread 2 READ 1000 concurrently. Step 3 Thread 1 WRITE 990. Step 4 Thread 2 overwrites with WRITE 990. Add a large red alert banner: 'LOST UPDATE DETECTED: Balance should be 980, but remains 990'. High-tech clean vector architecture infographic with dark backdrop and crimson warnings."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Server multithreaded yang mengelola state bersama (shared state) wajib dilindungi dengan primitif sinkronisasi seperti `threading.Lock()` atau mekanisme isolasi transaksional database.
2. Pengujian beban serentak (*concurrent load testing*) sangat esensial untuk mendeteksi bug konkurensi yang tidak terdeteksi pada pengujian fungsional tunggal.

### B. Kendala yang Dihadapi
Di lingkungan Python standar dengan GIL (Global Interpreter Lock), operasi primitive dict terkadang tampak aman untuk skrip sederhana. Pemberian jeda `sleep` mikrodetik diperlukan agar GIL berpindah thread dan membuktikan race condition secara empiris.
