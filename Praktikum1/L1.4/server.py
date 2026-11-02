from xmlrpc.server import SimpleXMLRPCServer

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.4 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def tambah(a, b):
    return a + b

if __name__ == "__main__":
    cetak_identitas()
    # logRequests=False agar overhead I/O terminal server tidak mengganggu benchmark
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    server.register_function(tambah, "tambah")
    print("[SERVER L1.4] Server Benchmark XML-RPC aktif pada port 8000...")
    server.serve_forever()
