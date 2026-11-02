import grpc
import akademik_v1_pb2 as pb2_v1
import akademik_v1_pb2_grpc as pb2_grpc_v1

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.3 (CLIENT SKEMA LAMA V1)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    print("[CLIENT V1] Berjalan menggunakan STUB LAMA (Hanya kenal: nim, nama, ipk).")
    print("[CLIENT V1] Menghubungi SERVER V2 (Mengirimkan field baru: prodi)...\n")

    with grpc.insecure_channel("localhost:50051") as channel:
        stub_lama = pb2_grpc_v1.LayananNilaiStub(channel)

        req = pb2_v1.MahasiswaRequest(nim="2023001")
        mhs = stub_lama.GetMahasiswa(req)

        print("--- HASIL PARSING DI SISI CLIENT LAMA ---")
        print(f"NIM  : {mhs.nim}")
        print(f"Nama : {mhs.nama}")
        print(f"IPK  : {mhs.ipk}")

        # Verifikasi keberadaan field prodi di objek client lama
        apakah_ada_prodi = hasattr(mhs, "prodi")
        print(f"\nApakah client lama memiliki atribut 'prodi'? {apakah_ada_prodi}")
        print("KESIMPULAN: Client lama TIDAK CRASH dan berhasil membaca seluruh field yang dikenalnya!")
        print("Protocol Buffers secara otomatis mengabaikan unknown fields (field nomor 4).")

if __name__ == "__main__":
    main()
