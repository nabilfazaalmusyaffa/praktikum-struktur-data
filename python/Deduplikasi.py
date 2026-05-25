def hapus_duplikat(data):
    sudah_ada = set()
    hasil = []
    
    for nilai in data:
        if nilai in sudah_ada:
            continue
        hasil.append(nilai)
        sudah_ada.add(nilai)
    
    return hasil

# Contoh
angka = [10, 20, 10, 30, 40, 20, 50]
print(hapus_duplikat(angka))