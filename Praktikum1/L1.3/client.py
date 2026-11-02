import xmlrpc.client
import datetime

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM RPC - LATIHAN L1.3 (SISI CLIENT)")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()

    print("\n[PENGUJIAN 1]: Mengirim objek datetime tanpa use_builtin_types=True")
    proxy_biasa = xmlrpc.client.ServerProxy("http://localhost:8000/")
    waktu_sekarang = datetime.datetime.now()
    try:
        res = proxy_biasa.terima_waktu(waktu_sekarang)
        print("Hasil:", res)
    except TypeError as e:
        print(f"[TERDETEKSI ERROR TYPEERROR]: {e}")
        print("Penjelasan: Objek datetime Python standar tidak dapat dimarshalling tanpa pembungkus DateTime atau use_builtin_types.")

    print("\n[PENGUJIAN 1b]: Solusi dengan xmlrpc.client.DateTime atau use_builtin_types=True")
    proxy_khusus = xmlrpc.client.ServerProxy("http://localhost:8000/", use_builtin_types=True)
    res_berhasil = proxy_khusus.terima_waktu(waktu_sekarang)
    print(f"Hasil setelah penyesuaian: {res_berhasil}")

    print("\n[PENGUJIAN 2]: Mengirim integer sangat besar (> 2^31 - 1)")
    batas_32bit = 2**31 - 1          # 2.147.483.647
    angka_sangat_besar = 2**31 + 500  # 2.147.484.147 (melebihi batas 32-bit signed)

    print(f"Batas Integer 32-bit bertanda : {batas_32bit}")
    print(f"Angka yang akan dikirim       : {angka_sangat_besar}")

    try:
        res_angka = proxy_biasa.terima_angka_besar(angka_sangat_besar)
        print("Hasil:", res_angka)
    except OverflowError as e:
        print(f"[TERDETEKSI ERROR OVERFLOWERROR]: {e}")
        print("Penjelasan: Spesifikasi dasar XML-RPC membatasi integer pada tag <i4> (32-bit signed int [-2^31 sampai 2^31 - 1]).")

    print("\n[PENGUJIAN 2b]: Solusi pengiriman angka besar (sebagai String atau Float)")
    res_str = proxy_biasa.terima_angka_besar(str(angka_sangat_besar))
    print(f"Hasil jika dikirim sebagai String: {res_str}")

if __name__ == "__main__":
    main()
