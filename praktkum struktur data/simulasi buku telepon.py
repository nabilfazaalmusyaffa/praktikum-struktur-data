phonebook = []

def tambah_kontak():
    nama = input("Masukkan nama: ")
    nomor = input("Masukkan nomor: ")
    phonebook.append([nama, nomor])

def tampilkan_kontak():
    for kontak in phonebook:
        print("Nama:", kontak[0], "| Nomor:", kontak[1])

def cari_kontak():
    cari = input("Cari nama: ")
    for kontak in phonebook:
        if kontak[0].lower() == cari.lower():
            print("Ditemukan:", kontak[1])
            return
    print("Kontak tidak ditemukan")

while True:
    print("\n1. Tambah\n2. Tampilkan\n3. Cari\n4. Keluar")
    pilih = input("Pilih menu: ")
    
    if pilih == "1":
        tambah_kontak()
    elif pilih == "2":
        tampilkan_kontak()
    elif pilih == "3":
        cari_kontak()
    elif pilih == "4":
        break