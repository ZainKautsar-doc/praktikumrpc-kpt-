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
    a, b = 2, 8
    print(f"Hitung {a} ^ {b} = {proxy.pangkat(a, b)}")

    a2, b2 = 5, 3
    print(f"Hitung {a2} ^ {b2} = {proxy.pangkat(a2, b2)}")

    print("\n--- PENGUJIAN FUNGSI AKAR ---")
    x1 = 81
    print(f"Hitung akar({x1}) = {proxy.akar(x1)}")

    x2 = 144
    print(f"Hitung akar({x2}) = {proxy.akar(x2)}")

    print("\n--- PENGUJIAN PENANGANAN ERROR (AKAR NEGATIF) ---")
    try:
        print("Mencoba akar(-16)...")
        print(proxy.akar(-16))
    except xmlrpc.client.Fault as e:
        print(f"[FAULT DARI SERVER]: {e.faultString}")

if __name__ == "__main__":
    main()
