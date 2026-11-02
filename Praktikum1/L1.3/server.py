from xmlrpc.server import SimpleXMLRPCServer
import datetime

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.3 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def terima_waktu(dt):
    """Menerima parameter datetime dan mencetak tipenya"""
    print(f"[SERVER] Menerima objek waktu: {dt} (Tipe: {type(dt)})")
    return f"Server berhasil menerima timestamp: {str(dt)}"

def terima_angka_besar(angka):
    """Menerima parameter bilangan bulat besar"""
    print(f"[SERVER] Menerima angka: {angka} (Tipe: {type(angka)})")
    return f"Angka {angka} berhasil diterima oleh server."

if __name__ == "__main__":
    cetak_identitas()
    # allow_none=True dan use_builtin_types=True di server
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True, use_builtin_types=True)
    server.register_introspection_functions()
    server.register_function(terima_waktu, "terima_waktu")
    server.register_function(terima_angka_besar, "terima_angka_besar")
    print("[SERVER L1.3] Server aktif di port 8000...")
    server.serve_forever()
