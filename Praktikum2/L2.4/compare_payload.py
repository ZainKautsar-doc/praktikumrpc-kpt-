import xmlrpc.client
import sys
import os

# Menghubungkan modul proto dari Praktikum dasar
sys.path.append(os.path.abspath(r"Praktikum2\Praktikum"))
import akademik_pb2 as pb

def cetak_identitas():
    print("=" * 60)
    print("PRAKTIKUM 2 gRPC - LATIHAN L2.4: PERBANDINGAN UKURAN PAYLOAD")
    print("Nama  : Zain Kautsar Ridha")
    print("NPM   : 247006111153")
    print("Kelas : EF")
    print("=" * 60)

def main():
    cetak_identitas()

    # 1. Objek Data Mahasiswa yang Sama
    nim = "2023001"
    nama = "Andi"
    ipk = 3.26

    # 2. Representasi Protocol Buffers (Biner)
    mhs_proto = pb.Mahasiswa(nim=nim, nama=nama, ipk=ipk)
    binary_payload = mhs_proto.SerializeToString()
    ukuran_proto = len(binary_payload)

    # 3. Representasi XML-RPC (Teks XML Response)
    # Marshalling XML-RPC dari dictionary/struct yang sama
    xml_data_dict = {"nim": nim, "nama": nama, "ipk": ipk}
    xml_payload_str = xmlrpc.client.dumps((xml_data_dict,), methodresponse=True)
    xml_payload_bytes = xml_payload_str.encode('utf-8')
    ukuran_xml = len(xml_payload_bytes)

    # 4. Tampilkan Rincian Isi Payload
    print("\n--- 1. PAYLOAD PROTOCOL BUFFERS (BINER) ---")
    print(f"Hex Representation : {binary_payload.hex(' ')}")
    print(f"Raw Bytes Output   : {binary_payload}")
    print(f"Ukuran Bersih      : {ukuran_proto} Bytes")

    print("\n--- 2. PAYLOAD XML-RPC (TEKS XML) ---")
    print(xml_payload_str.strip())
    print(f"Ukuran Bersih      : {ukuran_xml} Bytes")

    # 5. Analisis Perbandingan & Efisiensi
    selisih = ukuran_xml - ukuran_proto
    rasio_efisiensi = (ukuran_xml / ukuran_proto) if ukuran_proto > 0 else 0
    persen_penghematan = ((ukuran_xml - ukuran_proto) / ukuran_xml) * 100

    print("\n" + "=" * 65)
    print("RINGKASAN HASIL ANALISIS UKURAN PAYLOAD")
    print("=" * 65)
    print(f"{'Format Serialisasi':<25} | {'Ukuran Payload':<15} | {'Status Format':<20}")
    print("-" * 65)
    print(f"{'Protocol Buffers (gRPC)':<25} | {ukuran_proto:<3} Bytes        | {'Biner Terkompresi':<20}")
    print(f"{'XML-RPC':<25} | {ukuran_xml:<3} Bytes        | {'Teks XML Terbuka':<20}")
    print("=" * 65)
    print(f"Rasio Perbedaan       : Format XML ~{rasio_efisiensi:.1f}x lebih besar dibanding Protobuf.")
    print(f"Persentase Hemat Data : Protobuf menghemat {persen_penghematan:.2f}% bandwidth jaringan.")

if __name__ == "__main__":
    main()
