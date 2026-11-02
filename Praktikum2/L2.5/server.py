import time
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.5 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DATA = {
    "2023001": {"nama": "Andi", "ipk": 3.45},
    "2023002": {"nama": "Sari", "ipk": 3.82},
    "2023003": {"nama": "Budi", "ipk": 3.15},
    "2023004": {"nama": "Citra", "ipk": 3.90},
    "2023005": {"nama": "Dedi", "ipk": 3.20},
}

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        # Simulasi komputasi query database selama 0.2 detik per request
        time.sleep(0.2)
        mhs = DATA.get(request.nim, {"nama": f"Mhs-{request.nim}", "ipk": 3.00})
        print(f"[SERVER L2.5] Selesai memproses NIM: {request.nim} ({mhs['nama']})")
        return pb.Mahasiswa(nim=request.nim, nama=mhs["nama"], ipk=mhs["ipk"])

def serve():
    cetak_identitas()
    # Menggunakan pool 10 thread worker
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L2.5] Server gRPC Asinkron siap melayani di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
