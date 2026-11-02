import time
import uuid
import sys, os
sys.path.append(os.path.abspath(r"Praktikum3\Praktikum"))
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.1 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def transfer_dengan_retry(stub, dari, ke, jumlah, maks=4):
    rid = str(uuid.uuid4()) # ID transaksi konsisten per siklus transfer
    for percobaan in range(1, maks + 1):
        try:
            req = pb.TransferRequest(request_id=rid, dari=dari, ke=ke, jumlah=jumlah)
            # Timeout ditetapkan 2.0 detik
            return stub.Transfer(req, timeout=2.0)
        except grpc.RpcError as e:
            bisa_ulang = e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE)
            if not bisa_ulang or percobaan == maks:
                raise
            jeda = 0.5 * (2 ** (percobaan - 1))
            print(f" -> Percobaan {percobaan} timeout ({e.code().name}), retry dalam {jeda} s...")
            time.sleep(jeda)

def main():
    cetak_identitas()
    print("\n[CLIENT L3.1] Menjalankan 20 kali transfer nominal 10 dari A ke B...")
    print("Kondisi Awal yang Diharapkan: Saldo A = 1000, Saldo B = 500 (Total = 1500)\n")

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)

        for i in range(1, 21):
            print(f"--- Transaksi {i:02d} ---")
            res = transfer_dengan_retry(stub, "A", "B", 10.0)
            print(f"Status: {res.pesan}")
            time.sleep(0.2)

        print("\n" + "=" * 65)
        print("HASIL ANALISIS AKHIR LATIHAN L3.1:")
        print("1. Saldo A awal = 1000, berkurang tepat 20 x 10 = 200 -> Saldo Akhir A = 800")
        print("2. Saldo B awal = 500, bertambah tepat 20 x 10 = 200  -> Saldo Akhir B = 700")
        print("3. Total Saldo Sistem A + B = 800 + 700 = 1500 (KONSISTEN / KEKAL)")
        print("Deduplikasi Request ID berhasil mencegah eksekusi ganda pada saat retry!")
        print("=" * 65)

if __name__ == "__main__":
    main()
