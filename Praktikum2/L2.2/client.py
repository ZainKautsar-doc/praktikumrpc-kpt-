import time
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.2 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def generator_pesan_client():
    daftar_chat = [
        "Halo server, apakah nilai UTS Basis Data sudah final?",
        "Kapan jadwal perbaikan nilai mata kuliah Jaringan?",
        "Terima kasih atas konfirmasinya!"
    ]
    for chat in daftar_chat:
        pesan_obj = pb.Pesan(
            pengirim="Zain (NPM: 247006111153)",
            isi=chat,
            waktu=time.strftime("%H:%M:%S")
        )
        print(f"\n[CLIENT SEND ->] {pesan_obj.isi}")
        yield pesan_obj
        time.sleep(1.0)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)

        print("\n--- MEMULAI SESI BIDIRECTIONAL STREAMING (Diskusi) ---")
        stream_respons = stub.Diskusi(generator_pesan_client())

        for balasan in stream_respons:
            print(f"[CLIENT RECV <-] Dari: {balasan.pengirim} | Jam: {balasan.waktu}")
            print(f"                 Pesan: {balasan.isi}")

        print("\n--- SESI DISKUSI SELESAI SECARA AMAN ---")

if __name__ == "__main__":
    main()
