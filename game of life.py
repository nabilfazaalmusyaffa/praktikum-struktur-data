import time

# Ukuran papan
TINGGI = 6
LEBAR = 6

# 0 = mati, 1 = hidup
papan = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0]
]

def tampilkan(papan):
    for baris in papan:
        for sel in baris:
            if sel == 1:
                print("O", end=" ")
            else:
                print("-", end=" ")
        print()
    print()

def hitung_tetangga(papan, r, c):
    total = 0
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
                
            nr = r + i
            nc = c + j
            
            if 0 <= nr < TINGGI and 0 <= nc < LEBAR:
                total += papan[nr][nc]
                
    return total

def generasi_baru(papan):
    hasil = []
    
    for r in range(TINGGI):
        baris_baru = []
        for c in range(LEBAR):
            tetangga = hitung_tetangga(papan, r, c)
            
            if papan[r][c] == 1:
                if tetangga < 2 or tetangga > 3:
                    baris_baru.append(0)
                else:
                    baris_baru.append(1)
            else:
                if tetangga == 3:
                    baris_baru.append(1)
                else:
                    baris_baru.append(0)
        
        hasil.append(baris_baru)
    
    return hasil

# Jalankan simulasi
for gen in range(4):
    print("Generasi ke-", gen)
    tampilkan(papan)
    papan = generasi_baru(papan)
    time.sleep(1)
