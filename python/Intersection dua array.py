def cari_irisan(a, b):
    hasil = []
    set_b = set(b)
    
    for item in a:
        if item in set_b and item not in hasil:
            hasil.append(item)
    
    return hasil

# Contoh
list1 = [5, 6, 7, 8]
list2 = [7, 8, 9, 10]
print(cari_irisan(list1, list2))