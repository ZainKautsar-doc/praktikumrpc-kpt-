# LAPORAN PRAKTIKUM 1 — LATIHAN L1.3

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 1 (Latihan L1.3 — Pengujian Tipe Data datetime dan Bilangan Besar)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mengidentifikasi batasan tipe data pada spesifikasi standar XML-RPC.
2. Menganalisis penyebab terjadinya exception saat mengirim objek waktu dan bilangan bulat besar di atas 32-bit.
3. Menemukan dan menerapkan solusi rekayasa penanganan tipe data tersebut.

### B. Dasar Teori Singkat
Spesifikasi XML-RPC didefinisikan pada akhir tahun 1990-an dengan sekumpulan tipe data primitif terbatas:
- Tipe integer direpresentasikan melalui tag `<i4>` atau `<int>`, yaitu integer bertanda 32-bit (signed 32-bit integer) dengan jangkauan nilai $-2^{31}$ hingga $2^{31}-1$ ($-2.147.483.648$ sampai $2.147.483.647$). Bilangan di luar rentang ini tidak memiliki representasi tag resmi pada XML-RPC klasik.
- Tipe tanggal waktu direpresentasikan secara khusus dengan format ISO 8601 melalui tag `<dateTime.iso8601>`. Di Python, objek `datetime.datetime` membutuhkan flag `use_builtin_types=True` atau pembungkus `xmlrpc.client.DateTime` agar dapat diserialisasi ke tag tersebut.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Membuat fungsi penerima `terima_waktu(dt)` dan `terima_angka_besar(angka)` di server.
2. Mengirimkan objek `datetime.datetime.now()` dari client menggunakan `ServerProxy` standar dan mengamati timbulnya `TypeError`.
3. Menyesuaikan pemanggilan dengan konfigurasi `use_builtin_types=True` untuk membuktikan pengiriman berhasil.
4. Mengirimkan integer sebesar $2^{31} + 500 = 2.147.484.147$ dan mendokumentasikan munculnya `OverflowError`.
5. Menerapkan pengiriman angka besar dalam bentuk representasi string sebagai solusi interoperabilitas.

### B. Kode Program
#### Server (`server.py`):
```python
from xmlrpc.server import SimpleXMLRPCServer

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.3 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def terima_waktu(dt):
    return f"Server berhasil menerima timestamp: {str(dt)}"

def terima_angka_besar(angka):
    return f"Angka {angka} berhasil diterima oleh server."

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True, use_builtin_types=True)
    server.register_introspection_functions()
    server.register_function(terima_waktu, "terima_waktu")
    server.register_function(terima_angka_besar, "terima_angka_besar")
    print("[SERVER L1.3] Server aktif di port 8000...")
    server.serve_forever()
```

#### Client (`client.py`):
```python
import xmlrpc.client
import datetime

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.3 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    proxy_biasa = xmlrpc.client.ServerProxy("http://localhost:8000/")
    waktu_sekarang = datetime.datetime.now()

    # Uji 1: Datetime default
    try:
        proxy_biasa.terima_waktu(waktu_sekarang)
    except TypeError as e:
        print("[ERROR]:", e)

    # Uji 1b: Solusi Datetime
    proxy_khusus = xmlrpc.client.ServerProxy("http://localhost:8000/", use_builtin_types=True)
    print("Hasil datetime:", proxy_khusus.terima_waktu(waktu_sekarang))

    # Uji 2: Integer besar
    angka_besar = 2**31 + 500
    try:
        proxy_biasa.terima_angka_besar(angka_besar)
    except OverflowError as e:
        print("[ERROR OVERFLOW]:", e)

    # Uji 2b: Solusi string
    print("Hasil string:", proxy_biasa.terima_angka_besar(str(angka_besar)))

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), output pencetakan tipe data `datetime.datetime` saat flag aktif, dan tipe string dari bilangan besar.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, output tangkapan `TypeError: cannot marshal <class 'datetime.datetime'> objects`, keberhasilan pengiriman saat `use_builtin_types=True`, output tangkapan `OverflowError: int exceeds XML-RPC limits`, serta keberhasilan pengiriman bilangan besar saat dikonversi ke format string.

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Tabel Analisis Perilaku Tipe Data
| Kasus Uji | Tipe Data Asal | Respon Sistem Default | Exception Terpicu | Solusi Rekayasa |
|---|---|---|---|---|
| **Objek Waktu** | `datetime.datetime` | Gagal Marshalling | `TypeError` | Gunakan opsi `use_builtin_types=True` pada ServerProxy atau gunakan wrapper `xmlrpc.client.DateTime` |
| **Integer Besar** | `int` ($> 2^{31}-1$) | Melebihi batas 32-bit | `OverflowError` | Konversikan nilai menjadi tipe `string` sebelum transmisi atau kirim sebagai `float` |

### B. Prompt AI untuk Pembuatan Grafik / Visualisasi Perbandingan Tipe Data
Gunakan prompt berikut pada AI generator untuk membuat ilustrasi teknis:
> *"Create a professional technical diagram visualizing data type boundaries in RPC protocols. Show a comparison card layout: Card 1 shows 'XML-RPC Limitation' highlighting the 32-bit integer boundary ([-2^31, 2^31-1]), pointing to an Overflow error badge when exceeding 2,147,483,647. Card 2 shows datetime handling and the <dateTime.iso8601> tag conversion. Card 3 shows modern Protobuf/gRPC supporting native int64 and google.protobuf.Timestamp without overflow. Flat vector illustration, clean typography, navy blue and emerald green accents."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. Spesifikasi XML-RPC memiliki keterbatasan historis yang ketat, terutama pada batasan integer 32-bit yang dapat menimbulkan `OverflowError` pada komputasi modern.
2. Pengembang sistem terdistribusi harus memahami batasan skema serialisasi agar dapat melakukan adaptasi tipe data (seperti transformasi string atau pemanfaatan konfigurasi pustaka).

### B. Kendala yang Dihadapi
Format error `OverflowError` terjadi di client stub sebelum HTTP request dikirimkan ke jaringan, karena proses marshalling internal Python langsung menolak angka yang tidak muat dalam slot 4-byte integer.
