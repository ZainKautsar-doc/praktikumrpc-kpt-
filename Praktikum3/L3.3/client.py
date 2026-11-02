import uuid
from concurrent import futures
import sys, os
sys.path.append(os.path.abspath(r"Praktikum3\Praktikum"))
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.3 (CLIENT 50 TRANSFER SERENTAK)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def kirim_satu_transfer(nomor_tugas):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        req = pb.TransferRequest(
            request_id=str(uuid.uuid4()),
            dari="A",
            ke="B",
            jumlah=10.0
        )
        res = stub.Transfer(req, timeout=5.0)
        return (nomor_tugas, res.sukses, res.pesan)

def main():
    cetak_identitas()
    print("\n[CLIENT L3.3] Meluncurkan 50 transfer (nominal 10) secara serentak dari 10 client threads...")
    print("Kondisi Awal Ideal: Saldo A = 1000, Saldo B = 500 (Total = 1500)")
    print("Jika 50 transfer berhasil: Saldo A = 500, Saldo B = 1000 (Total HARUS 1500)\n")

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        tugas_list = [executor.submit(kirim_satu_transfer, i) for i in range(1, 51)]
        sukses_count = 0
        pesan_terakhir = ""

        for f in futures.as_completed(tugas_list):
            nomor, sukses, pesan = f.result()
            if sukses:
                sukses_count += 1
                pesan_terakhir = pesan

    print("\n" + "=" * 65)
    print("HASIL PENGUJIAN RACE CONDITION:")
    print("=" * 65)
    print(f"Total transfer terkirim : 50")
    print(f"Transfer berhasil       : {sukses_count}")
    print(f"Laporan Saldo Terakhir  : {pesan_terakhir}")
    print("\nKESIMPULAN: Karena proteksi 'with LOCK:' ditiadakan di server, terjadi")
    print("interleaving pada operasi pembacaan dan penulisan memory (Lost Update).")
    print("Total saldo sistem TIDAK LAGI 1500! Terjadi kerusakan data (Data Corruption).")
    print("=" * 65)

if __name__ == "__main__":
    main()
