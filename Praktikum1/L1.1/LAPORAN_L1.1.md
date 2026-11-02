# LAPORAN PRAKTIKUM 1 — LATIHAN L1.1

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 1 (Latihan L1.1 — Penambahan Fungsi Pangkat dan Akar)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mahasiswa mampu memperluas antarmuka fungsional pada server XML-RPC dengan mendaftarkan method baru (`pangkat` dan `akar`).
2. Mahasiswa mampu menguji pemanggilan fungsi jarak jauh dari client serta menangani respons normal maupun error validasi matematis.

### B. Dasar Teori Singkat
Remote Procedure Call (RPC) memungkinkan pemanggilan fungsi di mesin jarak jauh dengan abstraksi yang identik dengan pemanggilan lokal. Dalam XML-RPC, fungsi Python didaftarkan ke objek `SimpleXMLRPCServer` menggunakan `server.register_function()`. Saat client memanggil fungsi tersebut melalui objek stub (`ServerProxy`), argumen dikonversi menjadi representasi teks XML (marshalling), dikirim via HTTP POST, dieksekusi di server, dan hasilnya dikembalikan setelah diubah kembali ke tipe data Python (unmarshalling). Jika server melempar pengecualian (exception), pustaka XML-RPC server secara otomatis mengemasnya menjadi elemen `<fault>` XML-RPC standar.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Membuat berkas `server.py` yang mengimpor pustaka `xmlrpc.server` dan `math`.
2. Mendefinisikan fungsi `pangkat(a, b)` yang menghitung $a^b$ dan `akar(x)` yang menghitung $\sqrt{x}$ dengan validasi $x \ge 0$.
3. Mendaftarkan kedua fungsi tersebut ke instans `SimpleXMLRPCServer` pada port 8000.
4. Membuat berkas `client.py` yang menghubungkan `ServerProxy` ke alamat server.
5. Memanggil fungsi `pangkat` dan `akar` dengan beberapa variasi nilai, serta menguji penanganan error ketika memasukkan bilangan negatif.

### B. Kode Program
#### Server (`server.py`):
```python
from xmlrpc.server import SimpleXMLRPCServer
import math

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.1 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def tambah(a, b): return a + b
def kali(a, b): return a * b
def bagi(a, b):
    if b == 0: raise ValueError("Pembagian dengan nol")
    return a / b

def pangkat(a, b):
    return float(a ** b)

def akar(x):
    if x < 0:
        raise ValueError("Tidak dapat menghitung akar kuadrat dari bilangan negatif")
    return float(math.sqrt(x))

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()
    server.register_function(tambah, "tambah")
    server.register_function(kali, "kali")
    server.register_function(bagi, "bagi")
    server.register_function(pangkat, "pangkat")
    server.register_function(akar, "akar")
    print("[SERVER L1.1] Server XML-RPC aktif dan mendengarkan pada port 8000...")
    server.serve_forever()
```

#### Client (`client.py`):
```python
import xmlrpc.client

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.1 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", verbose=False)

    print("\n--- DAFTAR METHOD TERSEDIA DI SERVER ---")
    print(proxy.system.listMethods())

    print("\n--- PENGUJIAN FUNGSI PANGKAT ---")
    print("2 ^ 8 =", proxy.pangkat(2, 8))
    print("5 ^ 3 =", proxy.pangkat(5, 3))

    print("\n--- PENGUJIAN FUNGSI AKAR ---")
    print("akar(81) =", proxy.akar(81))
    print("akar(144) =", proxy.akar(144))

    print("\n--- PENGUJIAN PENANGANAN ERROR (AKAR NEGATIF) ---")
    try:
        print(proxy.akar(-16))
    except xmlrpc.client.Fault as e:
        print(f"[FAULT DARI SERVER]: {e.faultString}")

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan pencetakan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), status server aktif di port 8000, serta baris log HTTP POST saat method `system.listMethods`, `pangkat`, dan `akar` dieksekusi oleh client.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan pencetakan identitas mahasiswa, daftar method yang mencakup `pangkat` dan `akar`, hasil numerik `2 ^ 8 = 256.0`, `akar(81) = 9.0`, serta tangkapan pesan exception XML-RPC Fault saat mencoba `akar(-16)`.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Eksekusi
Penambahan method pada XML-RPC bersifat dinamis. Ketika fungsi `akar(-16)` dipanggil, server mengeksekusi percabangan `if x < 0: raise ValueError(...)`. Pengecualian ini ditangkap oleh dispatcher XML-RPC internal dan dikonversi menjadi struktur `<fault>` yang memuat `faultCode: 1` dan `faultString: <deskripsi error>`. Ini membuktikan transparansi transmisi error dari server ke client.

### B. Prompt AI untuk Pembuatan Ilustrasi / Diagram Alur
Gunakan prompt berikut pada AI generator (ChatGPT / Claude / Midjourney / Canva) untuk menghasilkan diagram alur:
> *"Create a professional, clean flowchart diagram for an XML-RPC Architecture showing remote function execution for 'pangkat(a, b)' and 'akar(x)'. The diagram must illustrate: 1. Client calling proxy.pangkat(2, 8), 2. Client Stub performing XML Marshalling into HTTP POST, 3. Network transmission over port 8000, 4. SimpleXMLRPCServer unmarshalling and executing Python math functions, and 5. Handling of XML Fault when evaluating negative square roots. Modern tech blueprint style with dark blue and white tones."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Penambahan fungsi baru pada server XML-RPC dapat dilakukan dengan mudah melalui `register_function()` tanpa perlu mengonfigurasi ulang arsitektur jaringan.
2. Validasi input matematika penting dilakukan di sisi server untuk menjaga integritas komputasi dan mengirimkan pesan kesalahan terstruktur kepada client.

### B. Kendala yang Dihadapi
Operasi akar kuadrat terhadap bilangan negatif dapat menyebabkan crash jika tidak ditangani dengan validasi eksplisit sebelum fungsi `math.sqrt()` dipanggil. Kendala ini diselesaikan dengan melempar `ValueError` deskriptif yang ditangkap client sebagai `xmlrpc.client.Fault`.
