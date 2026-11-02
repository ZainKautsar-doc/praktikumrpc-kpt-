import time
import uuid
import sys, os
sys.path.append(os.path.abspath(r"Praktikum3\Praktikum"))
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.2 (CLIENT DENGAN BUG UUID BARU)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def transfer_dengan_bug_uuid(stub, dari, ke, jumlah, maks=3):
    """
    BUG: uuid.uuid4() dipanggil DI DALAM LOOP PERCOBAAN RETRY.
    Setiap pengiriman ulang akan membawa Request ID baru!
    """
    for percobaan in range(1, maks + 1):
        rid_baru = str(uuid.uuid4()) # <- KESALAHAN FATAL: UUID baru di setiap percobaan
        try:
            req = pb.TransferRequest(request_id=rid_baru, dari=dari, ke=ke, jumlah=jumlah)
            return stub.Transfer(req, timeout=2.0)
        except grpc.RpcError as e:
            bisa_ulang = e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE)
            if not bisa_ulang or percobaan == maks:
                raise
            jeda = 0.5 * (2 ** (percobaan - 1))
            print(f" -> Percobaan {percobaan} timeout! Mengirim ulang dengan Request ID BARU: {rid_baru[:8]}...")
            time.sleep(jeda)

def main():
    cetak_identitas()
    print("\n[CLIENT L3.2] Menjalankan 20 transaksi transfer dengan BUG UUID BARU pada retry...")
    print("Tujuan: Mengamati terjadinya bencana TRANSFER GANDA (Double Debit).\n")

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)

        for i in range(1, 21):
            print(f"--- Transaksi {i:02d} ---")
            res = transfer_dengan_bug_uuid(stub, "A", "B", 10.0)
            print(f"Status: {res.pesan}")
            time.sleep(0.1)

        print("\n" + "=" * 65)
        print("HASIL ANALISIS LATIHAN L3.2:")
        print("Karena client meng-generate UUID baru pada saat retry, server TIDAK BISA")
        print("mengenali bahwa request tersebut adalah percobaan ulang dari transaksi yang sama.")
        print("Akibatnya, saldo terpotong lebih dari 200, dan sistem mengalami transfer ganda!")
        print("=" * 65)

if __name__ == "__main__":
    main()
