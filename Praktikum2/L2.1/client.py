import time
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.1 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def generator_nilai():
    daftar_data = [
        pb.NilaiRequest(nim="2023001", matkul="Algoritma Pemrograman", nilai=89.5),
        pb.NilaiRequest(nim="2023001", matkul="Struktur Data", nilai=94.0),
        pb.NilaiRequest(nim="2023001", matkul="Sistem Operasi", nilai=82.0),
        pb.NilaiRequest(nim="2023001", matkul="Kecerdasan Buatan", nilai=91.0)
    ]
    for item in daftar_data:
        print(f"[CLIENT STREAMING ->] Mengirim data: {item.matkul} = {item.nilai}")
        yield item
        time.sleep(0.4)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)

        print("\n--- PENGUJIAN L2.1: CLIENT STREAMING (KirimBanyakNilai) ---")
        print("Mengirimkan aliran batch data nilai ke server...")
        respons = stub.KirimBanyakNilai(generator_nilai())

        print("\n--- HASIL TANGGAPAN DARI SERVER ---")
        print(f"Status Sukses : {respons.sukses}")
        print(f"Pesan Server  : {respons.pesan}")

        print("\n--- VERIFIKASI DENGAN SERVER STREAMING (StreamNilai) ---")
        for n in stub.StreamNilai(pb.MahasiswaRequest(nim="2023001")):
            print(f"  * {n.matkul:<22}: {n.nilai}")

if __name__ == "__main__":
    main()
