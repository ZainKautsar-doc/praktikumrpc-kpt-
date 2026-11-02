import time
from concurrent import futures
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.2 (SISI SERVER)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

class LayananNilai(pb_grpc.LayananNilaiServicer):
    # Implementasi Latihan L2.2: Bidirectional Streaming
    def Diskusi(self, request_iterator, context):
        print("\n[SERVER DISKUSI] Sesi diskusi client terhubung!")
        for pesan_masuk in request_iterator:
            waktu_terima = time.strftime("%H:%M:%S")
            print(f"[{waktu_terima}] Pesan dari [{pesan_masuk.pengirim}]: {pesan_masuk.isi}")

            # Server langsung merespons setiap pesan yang masuk (full duplex)
            tanggapan = f"Halo {pesan_masuk.pengirim}, pesan Anda ('{pesan_masuk.isi}') telah diterima sistem akademik."
            yield pb.Pesan(
                pengirim="Server Akademik Bot",
                isi=tanggapan,
                waktu=time.strftime("%H:%M:%S")
            )

def serve():
    cetak_identitas()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LayananNilaiServicer_to_server(LayananNilai(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER L2.2] Server Chat Diskusi gRPC berjalan di port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
