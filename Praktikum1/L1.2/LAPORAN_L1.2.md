# LAPORAN PRAKTIKUM 1 — LATIHAN L1.2

## 1. Identitas
- **Nama Mahasiswa** : Zain Kautsar Ridha
- **NPM** : 247006111153
- **Kelas** : EF
- **Nomor Praktikum** : Praktikum 1 (Latihan L1.2 — Marshalling List dan Dictionary pada XML-RPC)

---

## 2. Tujuan dan Dasar Teori Singkat
### A. Tujuan
1. Mahasiswa memahami cara kerja transmisi tipe data majemuk (koleksi) seperti `list` dan `dictionary` melalui protokol XML-RPC.
2. Mahasiswa dapat menganalisis representasi XML `<array>` dan `<struct>` melalui inspeksi pesan mentah (verbose logging).

### B. Dasar Teori Singkat
Ketika melewatkan struktur data dinamis antar-bahasa atau antar-proses, RPC harus melakukan serialisasi (marshalling). Spesifikasi XML-RPC memetakan struktur data sebagai berikut:
- **Python `list` / `tuple`** dipetakan ke elemen `<array><data><value>...</value></data></array>`. Elemen-elemen di dalamnya disusun berurutan.
- **Python `dict` (Key-Value)** dipetakan ke elemen `<struct>`, di mana setiap pasangan kunci-nilai dibungkus dengan `<member><name>key</name><value>val</value></member>`.

---

## 3. Langkah Kerja dan Kode Program
### A. Langkah Kerja
1. Membuat fungsi `statistik(daftar)` di server yang menghitung nilai minimum, maksimum, dan rata-rata dari list yang diterima.
2. Mengembalikan hasil komputasi dalam bentuk dictionary Python.
3. Menjalankan server dan client dengan parameter `verbose=True` di sisi client.
4. Menganalisis potongan payload XML request (`<array>`) dan response (`<struct>`).

### B. Kode Program
#### Server (`server.py`):
```python
from xmlrpc.server import SimpleXMLRPCServer

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.2 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def statistik(daftar):
    if not isinstance(daftar, (list, tuple)):
        raise TypeError("Parameter harus berupa list atau tuple")
    if len(daftar) == 0:
        raise ValueError("Daftar angka tidak boleh kosong")

    return {
        "min": float(min(daftar)),
        "max": float(max(daftar)),
        "rata2": float(sum(daftar) / len(daftar))
    }

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()
    server.register_function(statistik, "statistik")
    print("[SERVER L1.2] Server Statistik XML-RPC aktif pada port 8000...")
    server.serve_forever()
```

#### Client (`client.py`):
```python
import xmlrpc.client

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.2 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", verbose=True)
    data_angka = [14, 88, 32, 95, 4, 61, 73]
    hasil = proxy.statistik(data_angka)
    print("\nHasil:", hasil)

if __name__ == "__main__":
    main()
```

---

## 4. Tangkapan Layar Hasil Eksekusi Server dan Client
- **[Keterangan Screenshot Server]:** Terminal server menampilkan identitas mahasiswa (Zain Kautsar Ridha / 247006111153), output log server menerima panggilan method `statistik`, dan mengembalikan status HTTP 200 OK ke client.
- **[Keterangan Screenshot Client]:** Terminal client menampilkan identitas mahasiswa, pencetakan verbose header HTTP POST, potongan body XML `<array>` yang dikirimkan, potongan body XML balasan `<struct>` dari server, dan hasil akhir pencetakan dictionary Python (`min: 4.0`, `max: 95.0`, `rata2: 52.43`).

---

## 5. Jawaban Pertanyaan Analisis dan Hasil Pengukuran

### A. Analisis Marshalling List dan Dictionary
Berdasarkan log verbose client, pengamatan struktural payload adalah sebagai berikut:
1. **Marshalling List (Request):**
   ```xml
   <param>
     <value><array><data>
       <value><int>14</int></value>
       <value><int>88</int></value>
       ...
     </data></array></value>
   </param>
   ```
2. **Marshalling Dictionary (Response):**
   ```xml
   <value><struct>
     <member>
       <name>min</name>
       <value><double>4.0</double></value>
     </member>
     <member>
       <name>max</name>
       <value><double>95.0</double></value>
     </member>
     <member>
       <name>rata2</name>
       <value><double>52.42857142857143</double></value>
     </member>
   </struct></value>
   ```
Struktur ini membuktikan bahwa XML-RPC membungkus setiap elemen kunci dan nilai secara eksplisit dengan tag pembuka dan penutup tersendiri.

### B. Prompt AI untuk Pembuatan Ilustrasi / Diagram Data Mapping
Gunakan prompt berikut pada AI generator untuk membuat infografis visual:
> *"Create a clean educational infographic diagram illustrating data serialization in XML-RPC. Show on the left side Python native data types: a List [14, 88, 32] and a Dictionary {'min': 4.0, 'max': 95.0}. Show in the center arrows pointing to the XML representation: <array><data>... and <struct><member><name>... with hierarchical XML indentation tree. On the right side, show deserialization back to client-side Python objects. Clean isometric modern UI design with blue, teal, and slate grey palette."*

---

## 6. Kesimpulan dan Kendala yang Dihadapi
### A. Kesimpulan
1. XML-RPC mampu menangani struktur data hierarkis majemuk (`list` dan `dict`) secara otomatis tanpa mengharuskan programmer menulis parser manual.
2. Konversi dari `list` ke `<array>` dan `dict` ke `<struct>` membuat struktur data netral platform, sehingga server Python dapat berkomunikasi dengan client Java, C#, atau PHP secara transparan.

### B. Kendala yang Dihadapi
Format `<struct>` XML memiliki overhead ukuran byte yang sangat masif karena string nama atribut (`min`, `max`, `rata2`) selalu diulang di dalam tag `<name>` pada setiap respon yang dikirimkan.
