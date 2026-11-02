import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)

        print("--- 1. PENGUJIAN UNARY: GetMahasiswa ---")
        mhs = stub.GetMahasiswa(pb.MahasiswaRequest(nim="2023001"))
        print(f"Data Mahasiswa: {mhs.nama} (NIM: {mhs.nim}) - IPK: {mhs.ipk}")

        print("\n--- 2. PENGUJIAN UNARY: TambahNilai ---")
        res_tambah = stub.TambahNilai(pb.NilaiRequest(nim="2023001", matkul="Komputasi Paralel", nilai=88.0))
        print(f"Status: {res_tambah.pesan}")

        print("\n--- 3. PENGUJIAN SERVER STREAMING: StreamNilai ---")
        print("Menerima aliran nilai dari server:")
        for n in stub.StreamNilai(pb.MahasiswaRequest(nim="2023001")):
            print(f"  * Mata Kuliah: {n.matkul:<20} | Nilai: {n.nilai}")

        print("\n--- 4. PENGUJIAN PENANGANAN ERROR (NOT FOUND) ---")
        try:
            stub.GetMahasiswa(pb.MahasiswaRequest(nim="9999"))
        except grpc.RpcError as e:
            print("Error tertangkap:", e.code(), "-", e.details())

if __name__ == "__main__":
    main()
