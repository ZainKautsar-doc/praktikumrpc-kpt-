import time
import random
import threading
from concurrent import futures
import sys, os
sys.path.append(os.path.abspath(r"Praktikum3\Praktikum"))
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.1 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

SALDO = {"A": 1000.0, "B": 500.0}
PROSES = {}
LOCK = threading.Lock()

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def Transfer(self, request, context):
        with LOCK:
            if request.request_id in PROSES:
                print(f"[SERVER L3.1] Duplikasi Request {request.request_id[:8]} terdeteksi! Mengembalikan balasan tersimpan.")
                return PROSES[request.request_id]

            if SALDO[request.dari] < request.jumlah:
                hasil = pb.StatusResponse(sukses=False, pesan="Saldo tidak cukup")
            else:
                SALDO[request.dari] -= request.jumlah
                SALDO[request.ke] += request.jumlah
                hasil = pb.StatusResponse(sukses=True, pesan=f"Saldo kini {SALDO}")
            PROSES[request.request_id] = hasil

        if random.random() < 0.35: # Peluang 35% response delay
            print(f"[SERVER L3.1] Delay buatan 3 detik untuk simulasi timeout...")
            time.sleep(3)

        return hasil

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L3.1] Server transfer aktif di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
