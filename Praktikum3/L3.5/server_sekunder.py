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
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.5 (SERVER SEKUNDER PORT 50052)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

class LayananSekunder(pb_grpc.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        print(f"[SERVER SEKUNDER :50052] FAILOVER BERHASIL! Melayani request NIM {request.nim}")
        return pb.Mahasiswa(nim=request.nim, nama="Andi (Dari Server FAILOVER :50052)", ipk=3.85)

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananSekunder(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("[SERVER SEKUNDER] Siaga aktif di port 50052 sebagai node Failover Cadangan...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
