import time
from concurrent import futures
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
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.3 (SERVER TANPA LOCK / RACE CONDITION)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

SALDO = {"A": 1000.0, "B": 500.0}

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def Transfer(self, request, context):
        # PERHATIKAN: with LOCK ditiadakan untuk membuktikan Race Condition
        saldo_a_lama = SALDO[request.dari]
        saldo_b_lama = SALDO[request.ke]

        # Jeda mikrodetik untuk memperbesar peluang context-switching antar thread
        time.sleep(0.001)

        if saldo_a_lama >= request.jumlah:
            SALDO[request.dari] = saldo_a_lama - request.jumlah
            # Simulasi delay interleaving antar mutasi rekening
            time.sleep(0.001)
            SALDO[request.ke] = saldo_b_lama + request.jumlah
            return pb.StatusResponse(sukses=True, pesan=f"OK. Saldo kini {SALDO}")
        else:
            return pb.StatusResponse(sukses=False, pesan="Saldo tidak cukup")

def serve():
    cetak_identitas()
    # Menggunakan 10 worker threads aktif serentak
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L3.3] Server transfer TANPA LOCK aktif di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
