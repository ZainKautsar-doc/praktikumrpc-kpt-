from xmlrpc.server import SimpleXMLRPCServer
import math

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.1 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def tambah(a, b):
    return a + b

def kali(a, b):
    return a * b

def bagi(a, b):
    if b == 0:
        raise ValueError("Pembagian dengan nol")
    return a / b

def pangkat(a, b):
    """Menghitung perpangkatan a dipangkatkan b (a^b)"""
    return float(a ** b)

def akar(x):
    """Menghitung nilai akar kuadrat dari bilangan x"""
    if x < 0:
        raise ValueError("Tidak dapat menghitung akar kuadrat dari bilangan negatif")
    return float(math.sqrt(x))

if __name__ == "__main__":
    cetak_identitas()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()

    # Registrasi method kalkulator dasar
    server.register_function(tambah, "tambah")
    server.register_function(kali, "kali")
    server.register_function(bagi, "bagi")

    # Registrasi method baru L1.1
    server.register_function(pangkat, "pangkat")
    server.register_function(akar, "akar")

    print("[SERVER L1.1] Server XML-RPC aktif dan mendengarkan pada port 8000...")
    server.serve_forever()
