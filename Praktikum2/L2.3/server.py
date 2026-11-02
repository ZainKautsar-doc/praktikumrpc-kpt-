from concurrent import futures
import grpc
import akademik_v2_pb2 as pb2_v2
import akademik_v2_pb2_grpc as pb2_grpc_v2

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.3 (SERVER SKEMA BARU V2)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DATA_V2 = {
    "2023001": {"nama": "Andi", "ipk": 3.45, "prodi": "Informatika"},
    "2023002": {"nama": "Sari", "ipk": 3.80, "prodi": "Sistem Informasi"}
}

class LayananNilaiV2(pb2_grpc_v2.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        mhs = DATA_V2.get(request.nim)
        if not mhs:
            context.abort(grpc.StatusCode.NOT_FOUND, "Mahasiswa tidak ditemukan")
        
        print(f"[SERVER V2] Mengirim data lengkap dengan field baru 'prodi': {mhs['prodi']}")
        return pb2_v2.Mahasiswa(
            nim=request.nim,
            nama=mhs["nama"],
            ipk=mhs["ipk"],
            prodi=mhs["prodi"] # Field baru nomor 4
        )

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc_v2.add_LayananNilaiServicer_to_server(LayananNilaiV2(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER V2] Server gRPC versi baru (V2) mendengarkan di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
