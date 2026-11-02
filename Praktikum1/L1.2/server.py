from xmlrpc.server import SimpleXMLRPCServer

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.2 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def statistik(daftar):
    """
    Menerima parameter berupa list angka dan mengembalikan
    dictionary berisi nilai min, max, dan rata2.
    """
    if not isinstance(daftar, (list, tuple)):
        raise TypeError("Parameter harus berupa list atau tuple")
    if len(daftar) == 0:
        raise ValueError("Daftar angka tidak boleh kosong")

    nilai_min = float(min(daftar))
    nilai_max = float(max(daftar))
    rata_rata = float(sum(daftar) / len(daftar))

    return {
        "min": nilai_min,
        "max": nilai_max,
        "rata2": rata_rata
    }

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()
    server.register_function(statistik, "statistik")
    print("[SERVER L1.2] Server Statistik XML-RPC aktif pada port 8000...")
    server.serve_forever()
