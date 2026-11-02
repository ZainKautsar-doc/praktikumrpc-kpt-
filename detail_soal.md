# PANDUAN DAN PENJELASAN PRAKTIKUM 1 SAMPAI 3: REMOTE PROCEDURE CALLS (RPC)
**Mata Kuliah:** Komputasi Paralel dan Terdistribusi  
**Penyusun Dokumen:** Zain Kautsar Ridha (NIM: 247006111153) — Kelas EF  

---

## DAFTAR ISI
1. [PRAKTIKUM 1: RPC Dasar dengan XML-RPC](#praktikum-1-rpc-dasar-dengan-xml-rpc)
   - [A. Konsep & Analisis Kode Dasar](#a-konsep--analisis-kode-dasar-praktikum-1)
   - [B. Penjelasan & Pembahasan Latihan Praktikum 1 (L1.1 – L1.5)](#b-penjelasan--pembahasan-latihan-praktikum-1)
   - [C. Jawaban Pertanyaan Analisis Praktikum 1](#c-jawaban-pertanyaan-analisis-praktikum-1)
2. [PRAKTIKUM 2: gRPC dan Protocol Buffers](#praktikum-2-grpc-dan-protocol-buffers)
   - [A. Konsep & Analisis Kode Dasar](#a-konsep--analisis-kode-dasar-praktikum-2)
   - [B. Penjelasan & Pembahasan Latihan Praktikum 2 (L2.1 – L2.5)](#b-penjelasan--pembahasan-latihan-praktikum-2)
3. [PRAKTIKUM 3: Concurrency, Timeout, dan Toleransi Kegagalan](#praktikum-3-concurrency-timeout-dan-toleransi-kegagalan)
   - [A. Konsep & Analisis Kode Dasar](#a-konsep--analisis-kode-dasar-praktikum-3)
   - [B. Penjelasan & Pembahasan Latihan Praktikum 3 (L3.1 – L3.5)](#b-penjelasan--pembahasan-latihan-praktikum-3)
   - [C. Jawaban Pertanyaan Analisis Praktikum 3](#c-jawaban-pertanyaan-analisis-praktikum-3)

---

# PRAKTIKUM 1: RPC Dasar dengan XML-RPC

## A. Konsep & Analisis Kode Dasar (Praktikum 1)

XML-RPC merupakan protokol Remote Procedure Call sederhana yang memanfaatkan format teks **XML** untuk mengkodekan data/parameter pemanggilan dan protokol **HTTP/1.1** sebagai media transmisi transport.

### 1. Sisi Server (`server_kalkulator.py`)
```python
from xmlrpc.server import SimpleXMLRPCServer

def tambah(a, b): return a + b
def kali(a, b): return a * b
def bagi(a, b):
    if b == 0:
        raise ValueError("Pembagian dengan nol")
    return a / b

server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
server.register_introspection_functions()
server.register_function(tambah, "tambah")
server.register_function(kali, "kali")
server.register_function(bagi, "bagi")
print("Server XML-RPC berjalan di port 8000...")
server.serve_forever()
```
* **Binding Host & Port:** `("0.0.0.0", 8000)` membuat server mendengarkan seluruh antarmuka jaringan yang aktif (bisa diakses via `localhost` maupun IP eksternal LAN).
* **Fungsi Introspeksi:** `register_introspection_functions()` memungkinkan client meminta metadata method yang tersedia melalui `system.listMethods()` dan `system.methodHelp()`.
* **Registrasi Fungsi:** `server.register_function(fn, "alias")` memetakan nama prosedur RPC yang dapat dipanggil dari luar ke fungsi Python internal.
* **Error Handling:** Saat fungsi `bagi()` memicu `ValueError`, pustaka XML-RPC server otomatis mengubah exception Python menjadi format paket `<fault>` XML-RPC dan mengirimkannya kembali ke client dengan kode kesalahan HTTP 200 OK.

### 2. Sisi Client (`client_kalkulator.py`)
```python
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", verbose=True)
print("Daftar method:", proxy.system.listMethods())
print("5 + 3 =", proxy.tambah(5, 3))
print("4 x 7 =", proxy.kali(4, 7))

try:
    print(proxy.bagi(10, 0))
except xmlrpc.client.Fault as e:
    print("Error dari server:", e.faultString)
```
* **Stub / Proxy:** Objek `ServerProxy` berperan sebagai **Client Stub**. Saat `proxy.tambah(5, 3)` dipanggil, objek proxy ini memotong (intercept) pemanggilan fungsi lokal, membungkus argumen ke teks XML (`marshalling`), dan mengirimkan HTTP POST.
* **Opsi `verbose=True`:** Menampilkan payload HTTP request header, payload body XML `<methodCall>`, respons server, dan payload body XML `<methodResponse>`.
* **Exception Mapping:** Kegagalan dari server ditangkap di client sebagai `xmlrpc.client.Fault`.

---

## B. Penjelasan & Pembahasan Latihan Praktikum 1

### L1.1: Menambahkan Fungsi `pangkat(a, b)` dan `akar(x)`
* **Tujuan:** Memperluas prosedur matematika di server dan menguji pemanggilannya dari client.
* **Penjelasan Teknis:**
  * Tambahkan pustaka `math` di sisi server.
  * Tambahkan pengecekan nilai negatif pada `akar(x)` agar melempar error deskriptif jika `x < 0`.
* **Implementasi Kode Server:**
  ```python
  import math

  def pangkat(a, b):
      return float(a ** b)

  def akar(x):
      if x < 0:
          raise ValueError("Tidak dapat menghitung akar dari bilangan negatif")
      return float(math.sqrt(x))

  server.register_function(pangkat, "pangkat")
  server.register_function(akar, "akar")
  ```
* **Implementasi Pemanggilan Client:**
  ```python
  print("2 ^ 8 =", proxy.pangkat(2, 8))       # Hasil: 256.0
  print("Akar 81 =", proxy.akar(81))          # Hasil: 9.0
  ```

---

### L1.2: Fungsi `statistik(daftar)` dan Pengamatan Marshalling XML
* **Tujuan:** Memahami bagaimana tipe data gabungan (koleksi) seperti `list` dan `dict` direpresentasikan dalam format XML.
* **Implementasi Kode Server:**
  ```python
  def statistik(daftar):
      if not daftar:
          raise ValueError("Daftar angka tidak boleh kosong")
      return {
          "min": min(daftar),
          "max": max(daftar),
          "rata2": sum(daftar) / len(daftar)
      }

  server.register_function(statistik, "statistik")
  ```
* **Implementasi Pemanggilan Client:**
  ```python
  hasil = proxy.statistik([12, 45, 67, 23, 89, 5])
  print("Statistik:", hasil)
  # Output: {'max': 89, 'min': 5, 'rata2': 40.166666666666664}
  ```
* **Analisis Marshalling XML:**
  * **Python `list`** dimarshalling menjadi tag XML `<array><data><value>...</value></data></array>`.
  * **Python `dict`** dimarshalling menjadi tag XML `<struct>` yang berisi sejumlah pasangan `<member><name>...</name><value>...</value></member>`.

---

### L1.3: Mengirim Objek `datetime` dan Bilangan Besar (> $2^{31}-1$)
* **Tujuan:** Mengetahui batas tipe data bawaan spesifikasi XML-RPC.
* **Pengujian 1 — Objek `datetime`:**
  * Secara default, jika mengirim `datetime.datetime.now()` tanpa konfigurasi khusus, XML-RPC client melempar `TypeError: cannot marshal <class 'datetime.datetime'> objects` kecuali parameter `use_builtin_types=True` diaktifkan pada `ServerProxy` dan server mendukung tag `<dateTime.iso8601>`.
* **Pengujian 2 — Bilangan Lebih dari $2^{31}-1$ (misal $3.000.000.000$):**
  * **Hasil:** Memicu `OverflowError: int exceeds XML-RPC limits`.
  * **Penyebab:** Spesifikasi dasar XML-RPC mendefinisikan tipe integer sebagai `<int>` atau `<i4>`, yaitu bilangan bulat bertanda 32-bit (range $-2.147.483.648$ s.d. $2.147.483.647$). Python mendukung integer arbitrary-precision (tak terbatas), tetapi parser XML-RPC menolak integer yang melampaui batas 32-bit kecuali dikirimkan sebagai string atau float.

---

### L1.4: Benchmark 100x Pemanggilan RPC vs Pemanggilan Lokal
* **Tujuan:** Mengukur overhead jaringan dan marshalling pada RPC dibandingkan eksekusi lokal pada CPU/RAM.
* **Implementasi Kode Pengujian:**
  ```python
  import time

  # 1. Uji Fungsi Lokal
  def lokal_tambah(a, b): return a + b

  t0 = time.perf_counter()
  for _ in range(100):
      lokal_tambah(5, 3)
  durasi_lokal = time.perf_counter() - t0

  # 2. Uji RPC (Remote)
  t1 = time.perf_counter()
  for _ in range(100):
      proxy.tambah(5, 3)
  durasi_rpc = time.perf_counter() - t1

  print(f"100x Panggilan Lokal : {durasi_lokal:.6f} detik (Rata-rata: {durasi_lokal/100*1000:.4f} ms)")
  print(f"100x Panggilan RPC   : {durasi_rpc:.6f} detik (Rata-rata: {durasi_rpc/100*1000:.4f} ms)")
  ```
* **Analisis Hasil:**
  * Panggilan lokal umumnya memakan waktu di bawah 0.1 milidetik untuk 100 iterasi.
  * Panggilan RPC melalui jaringan memerlukan waktu sekitar 100–300 milidetik (atau lebih jika antar-komputer LAN), karena setiap pemanggilan melibatkan pembentukan koneksi HTTP, serialisasi XML, transmisi socket, deserialisasi, dan round-trip time (RTT). Latensi RPC bisa **1000 hingga 10.000 kali lebih lambat** dibanding pemanggilan fungsi lokal.

---

### L1.5: Simulasi Server Dimatikan & Penanganan Error
* **Tujuan:** Mengamati perilaku client saat server tidak merespons (server mati).
* **Exception yang Muncul:**
  * `ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it` (dibungkus dalam `socket.error` atau `urllib.error.URLError`).
* **Implementasi Penanganan Error yang Sesuai:**
  ```python
  import xmlrpc.client
  import socket

  proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
  try:
      hasil = proxy.tambah(10, 20)
      print("Hasil:", hasil)
  except ConnectionRefusedError:
      print("ERROR: Server XML-RPC tidak aktif atau port tidak dapat dijangkau!")
  except xmlrpc.client.Fault as e:
      print(f"ERROR BISNIS DARI SERVER: [{e.faultCode}] {e.faultString}")
  except Exception as e:
      print(f"TERJADI KESALAHAN JARINGAN LAINNYA: {type(e).__name__} - {e}")
  ```

---

## C. Jawaban Pertanyaan Analisis Praktikum 1

> **Pertanyaan:** Berapa ukuran (byte) pesan XML untuk `tambah(5, 3)`? Berapa persen yang merupakan data sebenarnya dan berapa persen overhead format?

### 1. Struktur Payload XML Permintaan (`<methodCall>`)
```xml
<?xml version='1.0'?>
<methodCall>
<methodName>tambah</methodName>
<params>
<param>
<value><int>5</int></value>
</param>
<param>
<value><int>3</int></value>
</param>
</params>
</methodCall>
```
* **Ukuran Payload XML Permintaan:** $\approx 180 - 195$ byte (belum termasuk HTTP header $\approx 120$ byte).
* **Data Aktual:** Angka `5` dan `3` (dan nama method `tambah`) $\approx 2 - 8$ byte.

### 2. Struktur Payload XML Balasan (`<methodResponse>`)
```xml
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><int>8</int></value>
</param>
</params>
</methodResponse>
```
* **Ukuran Payload XML Balasan:** $\approx 125 - 135$ byte.
* **Data Aktual:** Angka `8` = 1 karakter (1 byte).

### 3. Persentase Overhead:
* Total payload per transaksi round-trip $\approx 320$ byte.
* Data riil murni (nilai 5, 3, dan hasil 8) hanya $\approx 3$ byte data integer.
* **Persentase Data Aktual:** $\frac{3}{320} \times 100\% \approx 0.94\%$.
* **Persentase Format Overhead (Tag XML & Whitespace):** $\approx 99.06\%$.
* **Kesimpulan Analisis:** XML-RPC memiliki tingkat pemborosan bandwidth (*overhead*) yang luar biasa besar karena format teks XML yang verbose, menjadikannya tidak efisien untuk aplikasi berlatensi rendah atau komputasi berkinerja tinggi.

---

# PRAKTIKUM 2: gRPC dan Protocol Buffers

## A. Konsep & Analisis Kode Dasar (Praktikum 2)

gRPC menggunakan **Protocol Buffers (Protobuf)** sebagai IDL dan transport **HTTP/2**. Karakteristik utamanya: skema strictly-typed, serialisasi biner sangat kompak, serta dukungan berbagai pola transmisi.

### 1. Kontrak Antarmuka (`akademik.proto`)
```protobuf
syntax = "proto3";
package akademik;

service LayananNilai {
  rpc GetMahasiswa (MahasiswaRequest) returns (Mahasiswa);       // Unary
  rpc TambahNilai  (NilaiRequest)     returns (StatusResponse);  // Unary
  rpc StreamNilai  (MahasiswaRequest) returns (stream Nilai);    // Server Streaming
}

message MahasiswaRequest { string nim = 1; }
message Mahasiswa        { string nim = 1; string nama = 2; double ipk = 3; }
message NilaiRequest     { string nim = 1; string matkul = 2; double nilai = 3; }
message Nilai            { string matkul = 1; double nilai = 2; }
message StatusResponse   { bool sukses = 1; string pesan = 2; }
```
* Tag angka (`= 1`, `= 2`) adalah **field numbers**, identifier biner unik untuk setiap field agar tidak perlu mengirim string nama field melalui jaringan.
* Keyword `stream` pada nilai balik `StreamNilai` menandakan pola **Server Streaming**.

### 2. Kompilasi Stub
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. akademik.proto
```
* `akademik_pb2.py`: Berisi kelas message Protobuf (`Mahasiswa`, `NilaiRequest`, dll.) yang menangani serialisasi biner.
* `akademik_pb2_grpc.py`: Berisi:
  * `LayananNilaiStub`: Kelas client proxy.
  * `LayananNilaiServicer`: Kelas dasar abstrak yang wajib di-inherit oleh server.

### 3. Server (`server_grpc.py`)
* Menggunakan `grpc.server(futures.ThreadPoolExecutor(max_workers=10))` untuk menangani hingga 10 request bersamaan dalam worker pool terpisah.
* Method `StreamNilai` menggunakan konstruksi `yield` untuk mengalirkan respons `Nilai` satu per satu ke client secara bertahap tanpa harus menunggu semua data terkumpul.

---

## B. Penjelasan & Pembahasan Latihan Praktikum 2

### L2.1: Client Streaming — `KirimBanyakNilai(stream NilaiRequest)`
* **Konsep:** Client mengirimkan banyak item secara berkelanjutan melalui satu koneksi stream, lalu server memprosesnya dan hanya mengembalikan **satu** ringkasan status di akhir.
* **Perubahan `.proto`:**
  ```protobuf
  rpc KirimBanyakNilai (stream NilaiRequest) returns (StatusResponse);
  ```
* **Implementasi di Server (`server_grpc.py`):**
  ```python
  def KirimBanyakNilai(self, request_iterator, context):
      jumlah_tersimpan = 0
      for req in request_iterator:
          if not 0 <= req.nilai <= 100:
              continue
          mhs = DATA.setdefault(req.nim, {"nama": "(baru)", "nilai": {}})
          mhs["nilai"][req.matkul] = req.nilai
          jumlah_tersimpan += 1
      return pb.StatusResponse(
          sukses=True, 
          pesan=f"Berhasil menyimpan {jumlah_tersimpan} data nilai."
      )
  ```
* **Implementasi di Client (`client_grpc.py`):**
  ```python
  def generate_nilai():
      daftar_nilai = [
          pb.NilaiRequest(nim="2023001", matkul="Algoritma", nilai=90.0),
          pb.NilaiRequest(nim="2023001", matkul="Struktur Data", nilai=85.0),
          pb.NilaiRequest(nim="2023001", matkul="Sistem Operasi", nilai=95.0),
      ]
      for item in daftar_nilai:
          yield item

  respons = stub.KirimBanyakNilai(generate_nilai())
  print("Hasil Client Streaming:", respons.pesan)
  ```

---

### L2.2: Bidirectional Streaming — `Diskusi(stream Pesan)`
* **Konsep:** Client dan server saling mengirim aliran pesan secara independen dan simultan melalui koneksi HTTP/2 full-duplex tunggal.
* **Perubahan `.proto`:**
  ```protobuf
  message Pesan {
    string pengirim = 1;
    string isi = 2;
    string waktu = 3;
  }

  // di dalam service LayananNilai
  rpc Diskusi (stream Pesan) returns (stream Pesan);
  ```
* **Implementasi di Server:**
  ```python
  def Diskusi(self, request_iterator, context):
      for pesan_masuk in request_iterator:
          print(f"[{pesan_masuk.pengirim}]: {pesan_masuk.isi}")
          yield pb.Pesan(
              pengirim="Server Bot",
              isi=f"Echo: Terima pesan '{pesan_masuk.isi}'",
              waktu=time.strftime("%H:%M:%S")
          )
  ```

---

### L2.3: Analisis Backward Compatibility pada Protobuf
* **Langkah Uji:** Tambahkan `string prodi = 4;` pada pesan `Mahasiswa` di server, kompilasi hanya di server, lalu panggil server menggunakan client lama.
* **Apakah Tetap Berjalan?** **Ya, program tetap berjalan normal tanpa error.**
* **Penjelasan Teori:** Protobuf dirancang untuk *forward & backward compatibility*. Protobuf menggunakan **field tag numbers** saat serialisasi biner, bukan nama variabel teks. Jika client lama menerima field nomor 4 yang tidak dikenal dalam skema lamanya, parser Protobuf client secara otomatis mengabaikan field tersebut (disimpan sebagai *unknown fields*) tanpa merusak proses parsing field yang sudah dikenal (nim, nama, ipk).

---

### L2.4: Komparasi Ukuran Payload Biner Protobuf vs XML-RPC
* **Pengujian Ukuran Protobuf:**
  ```python
  mhs = pb.Mahasiswa(nim="2023001", nama="Andi", ipk=3.26)
  serialized = mhs.SerializeToString()
  print("Ukuran byte Protobuf:", len(serialized))  # Hasil: ~20 - 24 bytes
  ```
* **Komparasi:**
  * **XML-RPC (Praktikum 1):** $\approx 250 - 300$ byte teks untuk data yang sama.
  * **gRPC Protobuf (Praktikum 2):** $\approx 22$ byte biner.
* **Kesimpulan:** Payload Protobuf sekitar **10 hingga 15 kali lebih hemat bandwidth** daripada XML-RPC karena Protobuf tidak mengikutsertakan nama tag dan mengemas tipe angka menggunakan representasi varint/IEEE-754 biner.

---

### L2.5: Pemanggilan Asinkron dengan `stub.GetMahasiswa.future(...)`
* **Implementasi Pengiriman 10 Permintaan Konkuren:**
  ```python
  import grpc
  import akademik_pb2 as pb
  import akademik_pb2_grpc as pb_grpc

  with grpc.insecure_channel("localhost:50051") as channel:
      stub = pb_grpc.LayananNilaiStub(channel)
      
      # 1. Kirim 10 request secara asinkron tanpa blocking
      daftar_future = []
      print("Mengirim 10 request asinkron...")
      for i in range(10):
          fut = stub.GetMahasiswa.future(pb.MahasiswaRequest(nim="2023001"))
          daftar_future.append(fut)

      # 2. Lakukan pekerjaan lain di thread utama jika ada...
      
      # 3. Kumpulkan hasil ketika masing-masing selesai
      for idx, fut in enumerate(daftar_future):
          mhs = fut.result()  # Blocking hanya saat mengambil hasil dari objek future
          print(f"Respons {idx+1}: {mhs.nama} - IPK {mhs.ipk}")
  ```

---

# PRAKTIKUM 3: Concurrency, Timeout, dan Toleransi Kegagalan

## A. Konsep & Analisis Kode Dasar (Praktikum 3)

Praktikum 3 berfokus pada masalah utama sistem terdistribusi nyata: **kegagalan jaringan**, **keterlambatan respon (latency spikes)**, dan **race conditions** pada shared memory server.

### 1. Operasi Transfer & Deduplikasi di Server
```python
PROSES = {}          # request_id -> StatusResponse
LOCK = threading.Lock()

def Transfer(self, request, context):
    with LOCK:
        if request.request_id in PROSES:    # Pengecekan Idempotensi / Semantik At-Most-Once
            return PROSES[request.request_id]
        if SALDO[request.dari] < request.jumlah:
            hasil = pb.StatusResponse(sukses=False, pesan="Saldo tidak cukup")
        else:
            SALDO[request.dari] -= request.jumlah
            SALDO[request.ke] += request.jumlah
            hasil = pb.StatusResponse(sukses=True, pesan=f"Saldo kini {SALDO}")
        PROSES[request.request_id] = hasil

    if random.random() < 0.3:
        time.sleep(3)      # Simulasi network delay melebihi batas timeout client (2.0s)
    return hasil
```
* **Kunci Pengamanan:** `with LOCK:` mencegah race condition saat dua thread mengubah data rekening secara simultan.
* **Simulasi Kegagalan Jaringan:** `time.sleep(3)` terjadi **setelah** saldo dimutasi. Hal ini mereplikasi skenario nyata di mana proses di server sudah selesai, namun paket balasan tidak sampai ke client tepat waktu.

### 2. Client dengan Timeout & Exponential Backoff Retry
```python
def transfer_dengan_retry(stub, dari, ke, jumlah, maks=3):
    rid = str(uuid.uuid4())   # ID unik transaksi dipertahankan untuk seluruh retry
    for percobaan in range(1, maks + 1):
        try:
            req = pb.TransferRequest(request_id=rid, dari=dari, ke=ke, jumlah=jumlah)
            return stub.Transfer(req, timeout=2.0)
        except grpc.RpcError as e:
            bisa_ulang = e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE)
            if not bisa_ulang or percobaan == maks:
                raise
            jeda = 0.5 * (2 ** (percobaan - 1))  # 0.5s, 1.0s, 2.0s ...
            print(f"Percobaan {percobaan} timeout ({e.code().name}), retry dalam {jeda}s")
            time.sleep(jeda)
```
* **Timeout (`timeout=2.0`):** Mencegah client blocking selamanya jika server lambat.
* **Exponential Backoff:** Meningkatkan jeda retry secara eksponensial guna menghindari membebani server yang sedang overload (*thundering herd problem*).

---

## B. Penjelasan & Pembahasan Latihan Praktikum 3

### L3.1: Uji 20 Kali Transfer dari A ke B (Kekekalan Saldo)
* **Kondisi Awal:** Saldo A = 1000, Saldo B = 500 (Total = 1500).
* **Eksekusi:** 20 kali pemanggilan transfer nominal 10 dengan deduplikasi aktif (`rid` tetap saat retry).
* **Hasil Pengamatan:**
  * Meskipun beberapa kali terjadi `DEADLINE_EXCEEDED` dan client melakukan retry, server mendeteksi `request_id` yang sama dari kamus `PROSES`.
  * Server tidak mendebit ulang saldo saat retry, melainkan mengembalikan hasil sebelumnya.
  * **Saldo Akhir:** Saldo A = 800, Saldo B = 700. Total saldo tetap tepat **1500**.

---

### L3.2: Simulasi Transfer Ganda (Generate UUID Baru di Setiap Percobaan)
* **Modifikasi Client:**
  ```python
  # SALAH: UUID di-generate ulang di dalam loop retry
  for percobaan in range(1, maks + 1):
      rid = str(uuid.uuid4())
  ```
* **Hasil Pengamatan:**
  * Ketika terjadi timeout 3 detik di server (padahal saldo A sudah terpotong 10), client menganggap operasi gagal dan mengirim request baru dengan `request_id` baru.
  * Server mengira ini adalah transaksi berbeda, sehingga memotong saldo A sekali lagi.
  * **Saldo Akhir:** Saldo A berkurang lebih dari 200 (misalnya menjadi 770 atau 750), dan total saldo sistem rusak. Ini membuktikan bahaya semantik *at-least-once* pada operasi non-idempoten tanpa Request ID yang persisten.

---

### L3.3: Uji Race Condition (Menghapus `with LOCK:`)
* **Modifikasi Server:** Bagian manipulasi `SALDO` dijalankan tanpa proteksi `with LOCK:`.
* **Eksekusi:** 50 transfer serentak dari 10 worker threads bersamaan via `ThreadPoolExecutor`.
* **Hasil Pengamatan:**
  * Terjadi **Lost Update**: Dua thread membaca saldo lama yang sama secara bersamaan, melakukan pengurangan/penambahan, lalu menimpa hasil thread lainnya.
  * **Total Saldo Akhir:** Total uang tidak lagi bernilai 1500 (bisa bertambah atau berkurang secara acak). Ini menunjukkan pentingnya mekanisme sinkronisasi concurrency pada shared state di lingkungan multithreaded RPC server.

---

### L3.4: Pengukuran Throughput dan Latensi untuk `max_workers` = 1, 4, 10
* **Skenario:** 200 request `GetMahasiswa` dari 20 client threads, dengan simulasi delay `time.sleep(0.1)` di server.

| max_workers | Waktu Total (detik) | Throughput (req/detik) | Latensi Rata-rata (ms) |
|:-----------:|:-------------------:|:----------------------:|:----------------------:|
| **1**       | $\approx 20.2\text{ s}$ | $\approx 9.9\text{ req/s}$  | $\approx 1010\text{ ms}$ |
| **4**       | $\approx 5.2\text{ s}$  | $\approx 38.4\text{ req/s}$ | $\approx 260\text{ ms}$  |
| **10**      | $\approx 2.1\text{ s}$  | $\approx 95.2\text{ req/s}$ | $\approx 105\text{ ms}$  |

* **Analisis:**
  * Pada `max_workers = 1`, server hanya memproses 1 request dalam satu waktu secara serial (antrean bottleneck panjang).
  * Menambah worker hingga 10 memungkinkan hingga 10 request diproses secara paralel, meningkatkan throughput mendekati 10 kali lipat dan memangkas waktu tunggu latensi client.

---

### L3.5: Failover Otomatis Dua Server (Port 50051 & 50052)
* **Konsep:** Jika server primer (port 50051) mengalami kegagalan / mati (`UNAVAILABLE`), client secara transparan mengalihkan stub ke server sekunder (port 50052).
* **Implementasi Client Failover:**
  ```python
  def panggil_dengan_failover(payload):
      daftar_server = ["localhost:50051", "localhost:50052"]
      for alamat in daftar_server:
          try:
              with grpc.insecure_channel(alamat) as channel:
                  stub = pb_grpc.LayananNilaiStub(channel)
                  return stub.GetMahasiswa(payload, timeout=1.0)
          except grpc.RpcError as e:
              if e.code() == grpc.StatusCode.UNAVAILABLE:
                  print(f"Server {alamat} mati. Mencoba server berikutnya...")
                  continue
              raise
      raise RuntimeError("Semua node server tidak dapat dijangkau!")
  ```

---

## C. Jawaban Pertanyaan Analisis Praktikum 3

> **Pertanyaan Analisis:** Server menyimpan `PROSES` di memori (RAM). Apa yang terjadi pada jaminan *at-most-once* jika server restart? Usulkan perbaikannya.

### 1. Masalah yang Terjadi Saat Server Restart
Variabel `PROSES = {}` disimpan di memori RAM (volatil). Jika server crash atau di-restart di tengah operasional:
1. Seluruh riwayat `request_id` yang telah diproses sebelumnya akan terhapus.
2. Jika client yang mengalami timeout mengirimkan kembali transaksi retry dengan `request_id` lama sesaat setelah server hidup kembali, server yang baru tidak lagi mengenali ID tersebut.
3. Server akan memperlakukan transaksi tersebut sebagai transaksi baru dan mengeksekusinya kembali.
4. **Jaminan semantik *at-most-once* runtuh dan turun kembali menjadi *at-least-once***, memicu eksekusi ganda dan korupsi data saldo.

### 2. Usulan Solusi & Perbaikan Arsitektur
* **Penyimpanan Terdistribusi / Cache Persisten (Redis / Memcached with Persistence):**
  Simpan pasangan `request_id: StatusResponse` ke dalam basis data in-memory terdistribusi seperti **Redis** dengan masa berlaku waktu (TTL) tertentu. Redis tetap menyimpan data di luar lifecycle proses server gRPC, sehingga server restart tidak menghapus cache deduplikasi.
* **Penyimpanan Transaksional Berbasis RDBMS / Write-Ahead Logging (WAL):**
  Catat `request_id` ke dalam tabel transaksi database (misalnya PostgreSQL atau MySQL) dengan *unique constraint*. Pengecekan dan eksekusi dilakukan dalam satu unit transaksi database ACID:
  ```sql
  INSERT INTO riwayat_transaksi (request_id, status, hasil) VALUES ('...', 'PROCESSED', '...')
  ```
  Jika terjadi duplikasi request setelah restart, database akan melempar *unique constraint violation*, sehingga server dapat langsung membaca hasil transaksi sebelumnya dari tabel tanpa mengeksekusi mutasi saldo lagi.
