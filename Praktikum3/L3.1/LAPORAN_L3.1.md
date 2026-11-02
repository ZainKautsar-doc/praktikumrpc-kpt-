# LAPORAN PRAKTIKUM 3 — LATIHAN L3.1

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 3 (Latihan L3.1 — Toleransi Kegagalan dan Konsistensi Saldo via Deduplikasi)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Membuktikan efektivitas semantik *at-most-once* pada operasi non-idempoten (transfer dana) di lingkungan jaringan yang tidak stabil.
2. Mengamati mekanisme kerja Request ID deduplication di server saat client melakukan *exponential backoff retry*.

### B. Dasar Teori Singkat
Pada jaringan terdistribusi, kegagalan komunikasi dapat terjadi saat request dikirimkan atau saat respons dikirimkan balik ke client. Jika respons hilang, client menganggap operasi gagal dan melakukan retry. Tanpa proteksi idempotensi, operasi non-idempoten akan dieksekusi berulang kali.
Dengan mengimplementasikan **Request ID (UUID)** yang identik pada setiap siklus retry dan menyimpannya di struktur `PROSES = {}`, server dapat mendeteksi paket duplikat dan langsung mengembalikan hasil eksekusi sebelumnya tanpa memotong saldo rekening untuk kedua kalinya.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Menyiapkan data saldo awal: `A = 1000.0` dan `B = 500.0` (Total saldo = 1500.0).
2. Menambahkan tabel in-memory `PROSES = {}` dan proteksi `with LOCK:` di server.
3. Menambahkan injeksi delay acak 3 detik pada server (`time.sleep(3)`) untuk memicu event `DEADLINE_EXCEEDED` di client.
4. Di sisi client, mengatur `timeout=2.0` detik dan meluncurkan 20 transaksi pemindahan dana nominal 10.
5. Memverifikasi saldo akhir: Saldo A harus berkurang tepat 200 dan saldo total harus tetap 1500.

### B. Kode Program
#### Server (`server.py`):
```python
import time, random, threading
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.1 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

SALDO = {"A": 1000.0, "B": 500.0}
PROSES = {}
LOCK = threading.Lock()

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def Transfer(self, request, context):
        with LOCK:
            if request.request_id in PROSES:
                print(f"[DUPLIKAT] Request ID {request.request_id[:8]}... diabaikan, return cache.")
                return PROSES[request.request_id]

            if SALDO[request.dari] < request.jumlah:
                hasil = pb.StatusResponse(sukses=False, pesan="Saldo tidak cukup")
            else:
                SALDO[request.dari] -= request.jumlah
                SALDO[request.ke] += request.jumlah
                hasil = pb.StatusResponse(sukses=True, pesan=f"Saldo kini {SALDO}")
            PROSES[request.request_id] = hasil

        if random.random() < 0.35:
            time.sleep(3) # Simulasi balasan terlambat
        return hasil

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L3.1] Berjalan di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

#### Client (`client.py`):
```python
import time, uuid
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.1 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def transfer_dengan_retry(stub, dari, ke, jumlah, maks=4):
    rid = str(uuid.uuid4())
    for percobaan in range(1, maks + 1):
        try:
            req = pb.TransferRequest(request_id=rid, dari=dari, ke=ke, jumlah=jumlah)
            return stub.Transfer(req, timeout=2.0)
        except grpc.RpcError as e:
            bisa_ulang = e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE)
            if not bisa_ulang or percobaan == maks: raise
            jeda = 0.5 * (2 ** (percobaan - 1))
            print(f" -> Percobaan {percobaan} gagal ({e.code().name}), retry dalam {jeda}s")
            time.sleep(jeda)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        for i in range(1, 21):
            res = transfer_dengan_retry(stub, "A", "B", 10.0)
            print(f"Transaksi {i:02d}: {res.pesan}")
            time.sleep(0.1)

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), mendeteksi request duplikat saat delay 3 detik terpicu, dan mengembalikan hasil dari memori tanpa mutasi saldo berulang.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, beberapa percobaan yang sempat mengalami `DEADLINE_EXCEEDED` dan berhasil pada percobaan kedua, serta konfirmasi saldo akhir A = 800 dan B = 700 (Total = 1500).

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Konsistensi Saldo
Hasil eksekusi 20 transaksi bernilai 10 menghasilkan saldo akhir:
$$\text{Saldo A} = 1000 - (20 \times 10) = 800.0$$
$$\text{Saldo B} = 500 + (20 \times 10) = 700.0$$
$$\text{Total Saldo Sistem} = 800.0 + 700.0 = 1500.0$$
Meskipun terjadi retry sebanyak $\approx 6-8$ kali akibat delay buatan di server, deduplikasi request_id berhasil menjaga kekekalan total saldo sistem secara sempurna.

### B. Prompt AI untuk Men-generate Diagram Idempotensi & Retry Backoff
Gunakan prompt berikut pada AI generator untuk membuat arsitektur visual alur retry aman:
> *"Create a professional system sequence diagram illustrating At-Most-Once RPC Semantics using Request ID Deduplication and Exponential Backoff. Show Client sending Request with UUID-1. Server processes transfer and debits saldo, but the response experiences high latency (3s delay). Client triggers 2.0s Deadline Exceeded, waits 0.5s exponential backoff, and retries with the SAME UUID-1. Server Deduplication Interceptor catches UUID-1 in Memory Cache, skips balance mutation, and returns cached StatusResponse. The final balance is completely conserved at 1500. Modern high-contrast tech diagram with neon cyan and amber signals."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Semantik at-most-once merupakan prasyarat mutlak untuk transaksi finansial atau operasi terdistribusi non-idempoten lainnya.
2. Kombinasi batas timeout terukur, exponential backoff, dan deduplikasi Request ID di server menghasilkan sistem yang toleran terhadap kegagalan jaringan (*fault-tolerant*).

### B. Kendala yang Dihadapi
Delay acak di server dapat memicu penumpukan thread jika client melakukan retry terlalu agresif tanpa adanya jeda backoff.
