import xmlrpc.client
import socket
import urllib.error
import time

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.5 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    print("\n[CLIENT] Memulai loop komunikasi ke server setiap 2 detik.")
    print("[CLIENT] Silakan matikan server (tekan Ctrl+C pada terminal server) untuk mengamati error handling.\n")

    iterasi = 1
    while True:
        try:
            print(f"[Iterasi {iterasi}] Mengirim permintaan tambah({iterasi}, 10)...")
            hasil = proxy.tambah(iterasi, 10)
            print(f" -> Berhasil! Hasil dari server: {hasil}")
        except ConnectionRefusedError as e:
            print(f" -> [PENANGANAN ERROR] ConnectionRefusedError: Server tidak aktif / koneksi ditolak.")
            print(f"    Detail: {e}")
            print("    Tindakan: Client menunggu server pulih atau beralih ke node cadangan.")
            break
        except (socket.error, urllib.error.URLError) as e:
            print(f" -> [PENANGANAN ERROR] Network Error: Terjadi kegagalan komunikasi socket.")
            print(f"    Detail: {e}")
            break
        except xmlrpc.client.Fault as e:
            print(f" -> [PENANGANAN ERROR] XML-RPC Fault: Kesalahan logika di server.")
            print(f"    Detail: [{e.faultCode}] {e.faultString}")
            break
        except Exception as e:
            print(f" -> [PENANGANAN ERROR] Terjadi error tak terduga: {type(e).__name__} - {e}")
            break

        iterasi += 1
        time.sleep(2)

if __name__ == "__main__":
    main()
