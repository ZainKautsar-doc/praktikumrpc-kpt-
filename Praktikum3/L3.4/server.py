import time
from concurrent import futures
import sys, os
sys.path.append(os.path.abspath(r"Praktikum3\Praktikum"))
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.4 (SERVER BENCHMARK THROUGHPUT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        # Sesuai modul: tambahkan time.sleep(0.1) untuk mensimulasikan beban I/O
        time.sleep(0.1)
        return pb.Mahasiswa(nim=request.nim, nama="Andi", ipk=3.75)

def run_server(workers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    return server

if __name__ == "__main__":
    cetak_identitas()
    workers_input = 10
    if len(sys.argv) > 1:
        workers_input = int(sys.argv[1])
    
    server = run_server(workers_input)
    print(f"[SERVER L3.4] Server aktif dengan max_workers = {workers_input} di port 50051...")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
