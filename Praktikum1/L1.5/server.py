from xmlrpc.server import SimpleXMLRPCServer

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.5 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def tambah(a, b):
    return a + b

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()
    server.register_function(tambah, "tambah")
    print("[SERVER L1.5] Server aktif di port 8000. Tekan Ctrl+C untuk simulasi server mati...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER L1.5] Server dimatikan oleh pengguna.")
