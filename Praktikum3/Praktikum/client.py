import time
import uuid
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def transfer_dengan_retry(stub, dari, ke, jumlah, maks=3):
    rid = str(uuid.uuid4()) # ID dipertahankan untuk seluruh siklus retry
    for percobaan in range(1, maks + 1):
        try:
            req = pb.TransferRequest(request_id=rid, dari=dari, ke=ke, jumlah=jumlah)
            return stub.Transfer(req, timeout=2.0)
        except grpc.RpcError as e:
            bisa_ulang = e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE)
            if not bisa_ulang or percobaan == maks:
                raise
            jeda = 0.5 * (2 ** (percobaan - 1))
            print(f"Percobaan {percobaan} gagal ({e.code().name}), coba ulang dalam {jeda} s...")
            time.sleep(jeda)

def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        print("Menguji pemanggilan transfer nominal 50 dari A ke B dengan retry backoff:")
        try:
            res = transfer_dengan_retry(stub, "A", "B", 50.0)
            print(f"Hasil: {res.pesan}")
        except Exception as e:
            print(f"Transfer gagal total: {e}")

if __name__ == "__main__":
    main()
