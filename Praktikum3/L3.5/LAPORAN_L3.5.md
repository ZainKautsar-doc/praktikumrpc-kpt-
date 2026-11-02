# LAPORAN PRAKTIKUM 3 — LATIHAN L3.5

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 3 (Latihan L3.5 — Pengayaan Arsitektur Failover Multi-Server)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mengimplementasikan mekanisme toleransi kegagalan tingkat lanjut berupa *Automatic Failover* antar-node server gRPC.
2. Memastikan ketersediaan layanan sistem terdistribusi (High Availability) tetap terjaga meskipun node server utama mengalami down/crash total.

### B. Dasar Teori Singkat
Dalam sistem terdistribusi misi-kritis (mission-critical), ketersediaan layanan (*availability*) dicapai melalui redundansi node. Client dilengkapi daftar alamat node (`endpoint discovery`). Ketika pemanggilan ke node primer mengembalikan kode error `StatusCode.UNAVAILABLE` atau mengalami timeout, client stub secara otomatis menangkap exception tersebut dan mengalihkan koneksi ke node sekunder (standby replica) secara transparan tanpa mengganggu alur pengalaman pengguna aplikasi.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Membuat dua program server independen: `server_primer.py` pada port 50051 dan `server_sekunder.py` pada port 50052.
2. Menulis skrip `client_failover.py` yang memiliki daftar alamat server `["localhost:50051", "localhost:50052"]`.
3. Mengatur loop pemanggilan rutin setiap 2 detik.
4. Menjalankan kedua server dan client.
5. Mematikan Server Primer secara mendadak dengan `Ctrl + C` dan memverifikasi perpindahan otomatis client ke Server Sekunder.

### B. Kode Program
#### Client Failover (`client_failover.py`):
```python
import time, grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.5 (CLIENT FAILOVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DAFTAR_SERVER = ["localhost:50051", "localhost:50052"]

def panggil_dengan_failover(req):
    for alamat in DAFTAR_SERVER:
        try:
            with grpc.insecure_channel(alamat) as channel:
                stub = pb_grpc.LayananNilaiStub(channel)
                return stub.GetMahasiswa(req, timeout=1.0)
        except grpc.RpcError as e:
            if e.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED):
                print(f" -> [FAILOVER] Node {alamat} UNAVAILABLE. Beralih ke cadangan...")
                continue
            raise
    raise RuntimeError("Seluruh node cluster mati!")
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server Primer & Sekunder]:** Menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153) di kedua terminal server, log server primer melayani transaksi awal hingga dihentikan (crash), dan log server sekunder langsung aktif menerima transaksi failover.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, deteksi status `UNAVAILABLE` pada port 50051 saat server primer mati, dan transisi sukses menerima respon dari `Andi (Dari Server FAILOVER :50052)`.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Jawaban Pertanyaan Analisis Modul Praktikum
> *Server menyimpan PROSES di memori. Apa yang terjadi pada jaminan at-most-once jika server restart? Usulkan perbaikannya.*
1. **Dampak Jika Server Restart:**
   - Variabel `PROSES = {}` disimpan di RAM (volatile memory).
   - Jika proses server restart atau mati, seluruh riwayat Request ID transaksi yang pernah dieksekusi akan lenyap.
   - Jika client yang sempat mengalami timeout mengirim ulang transaksi lama setelah server hidup kembali, server tidak lagi memiliki data deduplikasi. Transaksi akan dieksekusi ulang, sehingga **jaminan at-most-once runtuh dan turun kembali menjadi at-least-once (terjadi eksekusi ganda)**.
2. **Usulan Solusi Perbaikan Arsitektur:**
   - **Distributed Persistent Cache (Redis dengan AOF/RDB):** Simpan pasangan `request_id: StatusResponse` ke dalam Redis dengan Time-To-Live (TTL). Cache deduplikasi tetap ada meskipun proses server gRPC restart.
   - **Idempotency Table pada Relational Database:** Catat `request_id` pada tabel basis data (PostgreSQL/MySQL) dengan *Unique Constraint* di dalam transaksi ACID. Jika ada duplikasi request setelah restart, database menolak transaksi mutasi dan server langsung membaca hasil status dari tabel.

### B. Prompt AI untuk Men-generate Diagram Arsitektur Failover Cluster
Gunakan prompt berikut pada AI generator untuk membuat visualisasi arsitektur kluster:
> *"Create a professional system architecture diagram illustrating High Availability gRPC Failover with Persistent Deduplication. At the top, show a Client Application. In the middle, show Primary Server Node (:50051) marked with a Red Crash icon, and Secondary Standby Server Node (:50052) actively receiving the redirected traffic arrow labeled 'Automatic Failover Route'. At the bottom, show both servers connected to an External Persistent Redis Cluster labeled 'Shared Persistent PROSES Cache (TTL Idempotency)'. Clean cloud-native infrastructure style, dark theme, emerald green active lanes, amber backup routes."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Mekanisme failover multi-server meningkatkan ketersediaan (*availability*) sistem secara signifikan terhadap insiden kegagalan perangkat keras atau crash proses.
2. Deduplikasi in-memory harus ditingkatkan ke media penyimpanan terdistribusi persisten (Redis/Database) agar jaminan *at-most-once* bertahan melintasi siklus hidup server restart.

### B. Kendala yang Dihadapi
Peralihan koneksi antar-channel membutuhkan penyesuaian batas timeout yang tepat agar client tidak menunggu terlalu lama pada node yang sudah tidak aktif sebelum berpindah ke node cadangan.
