from concurrent import futures
import sys, os
sys.path.append(os.path.abspath(r"Praktikum3\Praktikum"))
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.5 (SERVER PRIMER PORT 50051)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

class LayananPrimer(pb_grpc.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        print(f"[SERVER PRIMER :50051] Melayani request NIM {request.nim}")
        return pb.Mahasiswa(nim=request.nim, nama="Andi (Dari Server Primer :50051)", ipk=3.85)

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananPrimer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER PRIMER] Berjalan aktif di port 50051. Tekan Ctrl+C untuk mensimulasikan crash!")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[SERVER PRIMER] Server Primer MATI (Crash Simulated).")

if __name__ == "__main__":
    serve()
