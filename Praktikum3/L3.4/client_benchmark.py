import time
from concurrent import futures
import sys, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRAKTIKUM_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Praktikum"))
if PRAKTIKUM_DIR not in sys.path:
    sys.path.insert(0, PRAKTIKUM_DIR)
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 3 gRPC - LATIHAN L3.4 (CLIENT BENCHMARK 200 REQ)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def satu_request(stub):
    t_start = time.perf_counter()
    req = pb.MahasiswaRequest(nim="2023001")
    stub.GetMahasiswa(req)
    t_end = time.perf_counter()
    return (t_end - t_start) * 1000 # dalam milidetik

def worker_task(jumlah_req_per_thread):
    latensi_list = []
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)
        for _ in range(jumlah_req_per_thread):
            lat = satu_request(stub)
            latensi_list.append(lat)
    return latensi_list

def main():
    cetak_identitas()
    total_request = 200
    jumlah_client_threads = 20
    req_per_thread = total_request // jumlah_client_threads

    print(f"\n[BENCHMARK CLIENT] Mengirim {total_request} request dari {jumlah_client_threads} concurrent threads...")
    print("Setiap request server memiliki delay buatan 0.1 detik (100 ms).")
    print("Memulai pengukuran waktu total...\n")

    t_awal = time.perf_counter()

    semua_latensi = []
    with futures.ThreadPoolExecutor(max_workers=jumlah_client_threads) as executor:
        tugas_list = [executor.submit(worker_task, req_per_thread) for _ in range(jumlah_client_threads)]
        for f in futures.as_completed(tugas_list):
            semua_latensi.extend(f.result())

    t_akhir = time.perf_counter()
    waktu_total = t_akhir - t_awal
    throughput = total_request / waktu_total
    latensi_rata_ms = sum(semua_latensi) / len(semua_latensi)

    print("=" * 65)
    print(f"HASIL PENGUKURAN KINERJA (TOTAL {total_request} PERMINTAAN)")
    print("=" * 65)
    print(f"Waktu Total Eksekusi : {waktu_total:.4f} detik")
    print(f"Throughput           : {throughput:.2f} req/s")
    print(f"Latensi Rata-rata    : {latensi_rata_ms:.2f} ms")
    print("=" * 65)

if __name__ == "__main__":
    main()
