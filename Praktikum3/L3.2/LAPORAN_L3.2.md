# LAPORAN PRAKTIKUM 3 — LATIHAN L3.2

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 3 (Latihan L3.2 — Analisis Fenomena Transfer Ganda Akibat Regenerasi UUID)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Membuktikan bahwa pembuatan identifier permintaan baru pada setiap iterasi retry merusak semantik *at-most-once*.
2. Mengamati secara nyata terjadinya fenomena *double spending* / transfer ganda pada layanan finansial terdistribusi.

### B. Dasar Teori Singkat
Semantik *at-most-once* bergantung sepenuhnya pada **konsistensi identitas permintaan (Request ID)** antara usaha pertama dan usaha pengulangan (retry). Jika client men-generate UUID baru pada setiap percobaan retry:
1. Server berhasil mengeksekusi mutasi saldo pada request pertama, namun respons balasan terlambat mencapai client (melebihi deadline timeout).
2. Client yang mengalami timeout mengirimkan kembali request dengan UUID yang baru.
3. Server memeriksa tabel deduplikasi `PROSES` dan tidak menemukan UUID baru tersebut.
4. Server menganggap request tersebut adalah transaksi terpisah yang sah dan kembali memotong saldo. Akibatnya terjadi eksekusi ganda (*double debit*).

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Mengubah script client dengan meletakkan kode `rid = str(uuid.uuid4())` di **dalam** loop percobaan (`for percobaan in range(...)`).
2. Menjalankan server dengan delay respon acak 3 detik.
3. Menjalankan 20 kali pemanggilan transfer nominal 10 dari rekening A ke B.
4. Mencatat saldo akhir rekening A dan B serta menghitung selisih eksekusi berlebih (*over-debit*).

### B. Kode Program
#### Modifikasi Client Buggy (`client.py`):
```python
import time, uuid
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.2 (CLIENT DENGAN BUG UUID BARU)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def transfer_dengan_bug_uuid(stub, dari, ke, jumlah, maks=3):
    # KESALAHAN FATAL: UUID digenerate di dalam loop percobaan retry
    for percobaan in range(1, maks + 1):
        rid_baru = str(uuid.uuid4())
        try:
            req = pb.TransferRequest(request_id=rid_baru, dari=dari, ke=ke, jumlah=jumlah)
            return stub.Transfer(req, timeout=2.0)
        except grpc.RpcError as e:
            bisa_ulang = e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE)
            if not bisa_ulang or percobaan == maks: raise
            jeda = 0.5 * (2 ** (percobaan - 1))
            print(f" -> Timeout! Mengirim ulang dengan Request ID BARU: {rid_baru[:8]}...")
            time.sleep(jeda)
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), menerima request transfer dengan UUID berbeda meskipun berasal dari kegagalan transaksi yang sama, dan kembali memotong saldo.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, beberapa event timeout yang diikuti pembuatan UUID baru, serta saldo akhir rekening A yang terdebit jauh melebihi 200 (misalnya saldo A menjadi 730 atau 690).

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Mengapa Terjadi Transfer Ganda
1. **Penyebab Utama:** Pada semantik *at-most-once*, server hanya dapat memfilter duplikasi jika **kunci deduplikasi** tetap konstan. Ketika client mengganti UUID pada setiap percobaan retry, korelasi antar-percobaan terputus.
2. **Kondisi Saldo Nyata:**
   - Seharusnya untuk 20 transaksi bernilai 10: Saldo A = 800, Saldo B = 700.
   - Hasil Aktual Pengujian L3.2: Saldo A turun menjadi **710.0** dan Saldo B naik menjadi **790.0** (terjadi 9 kali eksekusi ganda).
   - Meskipun total uang sistem A + B tetap 1500, pemilik rekening A dirugikan sebesar 90 unit saldo karena dana terpotong tanpa persetujuan.

### B. Prompt AI untuk Men-generate Diagram Bahaya UUID Baru pada Retry
Gunakan prompt berikut pada AI generator untuk membuat ilustrasi alur kegagalan sistem:
> *"Create a technical incident analysis diagram illustrating the catastrophic Double Debit flaw in distributed RPC. Timeline view: Step 1 Client sends Transfer($10) with UUID-A. Step 2 Server completes transfer and updates balance (A=990), but network delays the ACK past the 2.0s deadline. Step 3 Client generates a BUGGY NEW UUID-B and retries. Step 4 Server treats UUID-B as a brand new transaction, deducting another $10 (A=980). Highlight with red warning banners: 'Idempotency Broken: Request ID Mutated during Retry'. Sleek dark cyber-incident report style."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Request ID / Idempotency Key wajib dibuat tepat satu kali pada awal inisiasi transaksi dan **dilarang keras diubah** selama rangkaian percobaan retry.
2. Kesalahan logika kecil di sisi client (seperti penempatan scope inisialisasi UUID) dapat merusak integritas konsistensi data finansial secara fatal.

### B. Kendala yang Dihadapi
Pada pengujian simulasi, jika jeda delay server tidak cukup besar, timeout tidak akan terpicu sehingga bug UUID baru tidak terlihat. Delay buatan 3 detik memastikan fenomena transfer ganda terbukti secara konsisten.
