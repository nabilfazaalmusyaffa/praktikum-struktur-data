def karakter_ulang_pertama(teks):
    for i in range(len(teks)):
        if teks[i] in teks[i+1:]:
            return teks[i]
    return None

# Contoh
print(karakter_ulang_pertama("programming"))