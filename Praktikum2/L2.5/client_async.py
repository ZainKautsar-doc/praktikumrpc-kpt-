import time
import grpc
import akademik_pb2 as pb
import akademik_pb2_grpc as pb_grpc

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.5 (SISI CLIENT ASINKRON)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb_grpc.LayananNilaiStub(channel)

        daftar_nim = [f"202300{i}" for i in range(1, 11)]
        print(f"\n[CLIENT] Mempersiapkan 10 request untuk NIM: {daftar_nim}")

        # 1. Pengiriman Asinkron (Non-blocking)
        print("\n--- TAHAP 1: MENGIRIM 10 REQUEST SECARA ASINKRON (.future) ---")
        t_awal = time.perf_counter()
        daftar_future = []

        for nim in daftar_nim:
            req = pb.MahasiswaRequest(nim=nim)
            # Pemanggilan future() langsung me-return objek future seketika (non-blocking)
            fut = stub.GetMahasiswa.future(req)
            daftar_future.append((nim, fut))
            print(f" -> Permintaan untuk NIM {nim} terkirim (Non-blocking).")

        t_kirim_selesai = time.perf_counter()
        print(f"[CLIENT] Seluruh 10 request berhasil diluncurkan dalam: {(t_kirim_selesai - t_awal)*1000:.2f} ms")

        # 2. Pengumpulan Hasil (.result)
        print("\n--- TAHAP 2: MENGUMPULKAN RESPON DENGAN (.result()) ---")
        for idx, (nim, fut) in enumerate(daftar_future, 1):
            mhs = fut.result() # Mengambil hasil yang sudah siap
            print(f"Hasil {idx:02d} | NIM: {mhs.nim} | Nama: {mhs.nama:<15} | IPK: {mhs.ipk}")

        t_total = time.perf_counter() - t_awal
        print("\n" + "=" * 65)
        print("ANALISIS WAKTU EKSEKUSI ASINKRON")
        print("=" * 65)
        print(f"Waktu total 10 panggilan paralel asinkron : {t_total:.4f} detik")
        print(f"Estimasi jika dilakukan secara sinkron  : {10 * 0.2:.2f} detik (10 x 200 ms)")
        print(f"Efisiensi peningkatan kecepatan (Speedup) : ~{(10 * 0.2) / t_total:.1f}x lebih cepat!")
        print("=" * 65)

if __name__ == "__main__":
    main()
