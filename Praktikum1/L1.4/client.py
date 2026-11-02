import xmlrpc.client
import time

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.4 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def lokal_tambah(a, b):
    return a + b

def main():
    cetak_identitas()
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", verbose=False)

    N = 100
    print(f"\n[1] Menjalankan {N} kali pemanggilan fungsi LOKAL...")
    t0_lokal = time.perf_counter()
    for _ in range(N):
        hasil_lokal = lokal_tambah(5, 3)
    t1_lokal = time.perf_counter()
    durasi_lokal = t1_lokal - t0_lokal
    latensi_rata_lokal_ms = (durasi_lokal / N) * 1000

    print(f"[2] Menjalankan {N} kali pemanggilan fungsi RPC (REMOTE)...")
    t0_rpc = time.perf_counter()
    for _ in range(N):
        hasil_rpc = proxy.tambah(5, 3)
    t1_rpc = time.perf_counter()
    durasi_rpc = t1_rpc - t0_rpc
    latensi_rata_rpc_ms = (durasi_rpc / N) * 1000

    print("\n" + "=" * 65)
    print("HASIL PENGUKURAN KINERJA (100 KALI ITERASI)")
    print("=" * 65)
    print(f"{'Metode Pemanggilan':<25} | {'Waktu Total (detik)':<20} | {'Rata-rata (ms)':<15}")
    print("-" * 65)
    print(f"{'Fungsi Lokal (CPU/RAM)':<25} | {durasi_lokal:<20.6f} | {latensi_rata_lokal_ms:<15.6f}")
    print(f"{'Remote Procedure Call':<25} | {durasi_rpc:<20.6f} | {latensi_rata_rpc_ms:<15.6f}")
    print("=" * 65)

    rasio = durasi_rpc / (durasi_lokal if durasi_lokal > 0 else 1e-9)
    print(f"\nKesimpulan Rasio: Pemanggilan RPC lebih lambat ~{rasio:.1f} kali dibanding fungsi lokal.")

if __name__ == "__main__":
    main()
