def cek_anagram(kata1, kata2):
    if sorted(kata1) == sorted(kata2):
        return True
    return False

# Contoh
print(cek_anagram("evil", "vile"))