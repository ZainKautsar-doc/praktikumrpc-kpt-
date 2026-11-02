import time
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.1 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

DATA = {
    "2023001": {"nama": "Andi", "nilai": {"Basis Data": 85.0, "Jaringan": 78.0}},
    "2023002": {"nama": "Sari", "nilai": {"Basis Data": 92.0}},
}

class LayananNilai(pb_grpc.LayananNilaiServicer):
    def GetMahasiswa(self, request, context):
        mhs = DATA.get(request.nim)
        if mhs is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"NIM {request.nim} tidak ditemukan")
        daftar = list(mhs["nilai"].values())
        ipk = sum(daftar) / len(daftar) / 25 if daftar else 0.0
        return pb.Mahasiswa(nim=request.nim, nama=mhs["nama"], ipk=round(ipk, 2))

    def TambahNilai(self, request, context):
        if not 0 <= request.nilai <= 100:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Nilai harus 0–100")
        mhs = DATA.setdefault(request.nim, {"nama": "(baru)", "nilai": {}})
        mhs["nilai"][request.matkul] = request.nilai
        return pb.StatusResponse(sukses=True, pesan="Nilai tersimpan")

    def StreamNilai(self, request, context):
        mhs = DATA.get(request.nim)
        if mhs is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "NIM tidak ditemukan")
        for matkul, nilai in mhs["nilai"].items():
            yield pb.Nilai(matkul=matkul, nilai=nilai)
            time.sleep(0.3)

    # Implementasi Latihan L2.1: Client Streaming
    def KirimBanyakNilai(self, request_iterator, context):
        jumlah_sukses = 0
        nim_terakhir = ""
        for req in request_iterator:
            nim_terakhir = req.nim
            if not 0 <= req.nilai <= 100:
                print(f"[SERVER WARN] Nilai {req.nilai} tidak valid untuk matkul {req.matkul}, dilewati.")
                continue
            mhs = DATA.setdefault(req.nim, {"nama": "(Mahasiswa Baru)", "nilai": {}})
            mhs["nilai"][req.matkul] = req.nilai
            jumlah_sukses += 1
            print(f"[SERVER L2.1] Menyimpan nilai: NIM {req.nim} | {req.matkul}: {req.nilai}")

        return pb.StatusResponse(
            sukses=True,
            pesan=f"Berhasil mengunggah dan menyimpan {jumlah_sukses} nilai untuk mahasiswa."
        )

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L2.1] Server gRPC aktif di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
