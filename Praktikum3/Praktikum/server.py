import time
import random
import threading
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

SALDO = {"A": 1000.0, "B": 500.0}
PROSES = {} # request_id -> StatusResponse
LOCK = threading.Lock()

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def Transfer(self, request, context):
        with LOCK:
            # Pengecekan deduplikasi (At-Most-Once)
            if request.request_id in PROSES:
                print(f"[SERVER DUPLIKAT] Request ID {request.request_id[:8]}... sudah diproses sebelumnya. Mengembalikan respons tersimpan.")
                return PROSES[request.request_id]

            if SALDO[request.dari] < request.jumlah:
                hasil = pb.StatusResponse(sukses=False, pesan=f"Saldo {request.dari} tidak cukup")
            else:
                SALDO[request.dari] -= request.jumlah
                SALDO[request.ke] += request.jumlah
                hasil = pb.StatusResponse(sukses=True, pesan=f"Transfer berhasil. Saldo: {SALDO}")
            
            PROSES[request.request_id] = hasil

        # Simulasi network delay acak 3 detik (melebihi timeout client 2.0s)
        if random.random() < 0.3:
            print(f"[SERVER DELAY] Mensimulasikan jeda balasan 3 detik untuk Request {request.request_id[:8]}...")
            time.sleep(3)

        return hasil

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server gRPC Praktikum 3 berjalan di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
