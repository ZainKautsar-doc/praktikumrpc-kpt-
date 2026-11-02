import time
import sys, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRAKTIKUM_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Praktikum"))
if PRAKTIKUM_DIR not in sys.path:
    sys.path.insert(0, PRAKTIKUM_DIR)
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.5 (CLIENT DENGAN FAILOVER OTOMATIS)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DAFTAR_SERVER = ["localhost:50051", "localhost:50052"]

def panggil_dengan_failover(req):
    for alamat in DAFTAR_SERVER:
        try:
            with grpc.insecure_channel(alamat) as channel:
                stub = pb_grpc.LayananNilaiStub(channel)
                # Timeout singkat 1.0 detik untuk deteksi failover cepat
                return stub.GetMahasiswa(req, timeout=1.0)
        except grpc.RpcError as e:
            if e.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED):
                print(f" -> [FAILOVER DETECTED] Node {alamat} gagal ({e.code().name}). Beralih ke node berikutnya...")
                continue
            raise
    raise RuntimeError("Seluruh node cluster server (Primer & Sekunder) tidak dapat dijangkau!")

def main():
    cetak_identitas()
    print("\n[CLIENT L3.5] Memulai pemanggilan rutin setiap 2 detik ke cluster server.")
    print("1. Server Primer aktif di port 50051")
    print("2. Server Sekunder siaga di port 50052")
    print("Silakan matikan Server Primer (Ctrl+C di terminal 50051) untuk melihat failover otomatis!\n")

    iterasi = 1
    while True:
        try:
            req = pb.MahasiswaRequest(nim=f"202300{iterasi}")
            print(f"[Iterasi {iterasi:02d}] Mengirim permintaan GetMahasiswa...")
            res = panggil_dengan_failover(req)
            print(f" -> Berhasil diterima dari: {res.nama} (IPK: {res.ipk})")
        except Exception as e:
            print(f" -> Fatal Error: {e}")
            break

        iterasi += 1
        time.sleep(2)

if __name__ == "__main__":
    main()
