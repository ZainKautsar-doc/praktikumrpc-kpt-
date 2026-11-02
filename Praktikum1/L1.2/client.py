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
    # verbose=True diaktifkan untuk mengamati struktur marshalling tag XML mentah
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", verbose=True)

    data_angka = [14, 88, 32, 95, 4, 61, 73]
    print(f"\n[CLIENT] Mengirim list data angka: {data_angka}")
    print("[CLIENT] Mengamati proses transmisi HTTP & XML (Verbose Mode)...\n")

    hasil = proxy.statistik(data_angka)

    print("\n" + "=" * 60)
    print("[CLIENT] HASIL DESERIALISASI DARI SERVER (DICTIONARY PYTHON):")
    print(f"Nilai Minimum : {hasil['min']}")
    print(f"Nilai Maximum : {hasil['max']}")
    print(f"Rata-rata     : {hasil['rata2']:.2f}")
    print("Tipe data kembalian:", type(hasil))
    print("=" * 60)

if __name__ == "__main__":
    main()
