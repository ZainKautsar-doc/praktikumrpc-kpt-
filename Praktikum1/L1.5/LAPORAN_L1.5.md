# LAPORAN PRAKTIKUM 1 — LATIHAN L1.5

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 1 (Latihan L1.5 — Penanganan Kegagalan Jaringan dan Server Mati)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mengamati exception yang muncul ketika koneksi RPC terputus secara mendadak akibat server mati (*abrupt crash*).
2. Mengimplementasikan teknik *fault tolerance* dan penanganan eksepsi jaringan bertingkat di sisi client.

### B. Dasar Teori Singkat
Salah satu karakteristik pembeda utama antara pemanggilan lokal dan Remote Procedure Call adalah **kegagalan parsial (*partial failure*)**. Pada fungsi lokal, pemanggil dan pemegang fungsi berada dalam satu proses yang sama. Pada RPC, server dapat mengalami crash sementara client tetap berjalan.
Ketika server mati, lapisan transport TCP di sistem operasi server akan merespons dengan paket TCP RST (*Reset*), atau jika server mati sepenuhnya, tidak ada proses yang mendengarkan port tersebut. Hal ini menyebabkan client stub Python melemparkan eksepsi `ConnectionRefusedError` (WinError 10061 di Windows / Errno 111 di Linux) yang dibungkus di dalam modul `socket` atau `urllib`.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Membuat `server.py` yang melayani pemanggilan fungsi `tambah(a, b)`.
2. Membuat `client.py` yang mengirimkan pemanggilan RPC secara berulang dalam loop interval 2 detik.
3. Menjalankan server dan client bersamaan hingga transaksi awal sukses.
4. Mematikan terminal server menggunakan kombinasi tombol `Ctrl + C`.
5. Mengamati jenis exception yang muncul pada client dan mengonfirmasi blok `try...except` berhasil menangkap `ConnectionRefusedError`.

### B. Kode Program
#### Server (`server.py`):
```python
from xmlrpc.server import SimpleXMLRPCServer

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.5 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def tambah(a, b): return a + b

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()
    server.register_function(tambah, "tambah")
    print("[SERVER L1.5] Server aktif di port 8000...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER L1.5] Server dihentikan oleh pengguna.")
```

#### Client (`client.py`):
```python
import xmlrpc.client
import socket
import urllib.error
import time

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.5 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    iterasi = 1
    while True:
        try:
            print(f"[Iterasi {iterasi}] Mengirim permintaan tambah({iterasi}, 10)...")
            hasil = proxy.tambah(iterasi, 10)
            print(f" -> Berhasil! Hasil dari server: {hasil}")
        except ConnectionRefusedError as e:
            print(f" -> [PENANGANAN ERROR] ConnectionRefusedError: Server mati.")
            print(f"    Detail: {e}")
            break
        except (socket.error, urllib.error.URLError) as e:
            print(f" -> [PENANGANAN ERROR] Network Error: {e}")
            break
        except xmlrpc.client.Fault as e:
            print(f" -> [PENANGANAN ERROR] Server Fault: {e.faultString}")
            break
        iterasi += 1
        time.sleep(2)

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), melayani request iterasi awal, kemudian dihentikan secara sengaja dengan `Ctrl + C` menampilkan status shutdown.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, mencetak keberhasilan pengiriman iterasi 1 dan 2, kemudian pada iterasi berikutnya ketika server mati langsung mencetak blok tangkapan `ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it` tanpa membuat program client crash/force close.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Jenis Exception & Mitigasi
1. **Exception yang Muncul:**
   - Di lingkungan Windows: `ConnectionRefusedError: [WinError 10061]`
   - Di lingkungan Linux/macOS: `ConnectionRefusedError: [Errno 111] Connection refused`
   - Dalam hirarki exception Python, error ini merupakan turunan dari `OSError` dan `socket.error`.
2. **Strategi Mitigasi Terdistribusi:**
   - **Retry dengan Exponential Backoff:** Client mencoba menghubungi server kembali beberapa saat kemudian dengan jeda waktu yang meningkat secara bertahap.
   - **Circuit Breaker & Fallback:** Jika server tetap mati setelah ambang batas tertentu, alihkan pemanggilan ke node server cadangan (failover).

### B. Prompt AI untuk Men-generate Diagram Fault Tolerance / Circuit Breaker
Gunakan prompt berikut pada AI generator untuk membuat arsitektur visual penanganan error:
> *"Create a technical state diagram and system architecture graphic illustrating RPC Fault Tolerance. Show a Client Application invoking a remote server. Stage 1 shows Normal Flow: HTTP POST 200 OK. Stage 2 shows Server Failure: server process crashes, OS emits TCP RST packet. Stage 3 shows Client Exception Handler intercepting ConnectionRefusedError, triggering Exponential Backoff Retry and activating a Failover Route to Secondary Backup Server. Professional dark mode architecture diagram with vibrant warning badges in amber and neon red."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Penanganan eksepsi jaringan (`ConnectionRefusedError` dan `socket.error`) merupakan komponen wajib dalam arsitektur RPC untuk mencegah client berhenti tiba-tiba saat terjadi kegagalan parsial pada node server.
2. Isolasi kegagalan pada RPC memungkinkan sistem client menerapkan strategi pemulihan otomatis seperti pengulangan terencana atau pengalihan rute (*failover*).

### B. Kendala yang Dihadapi
Jika client tidak membungkus pemanggilan remote dengan penanganan error jaringan spesifik, exception level OS akan menyebabkan unhandled crash pada thread utama aplikasi client.
