class Array:
    def __init__(self, capacity):
        """
        Membuat array dengan kapasitas tetap.
        Semua elemen diinisialisasi dengan None.
        """
        if capacity <= 0:
            raise ValueError("Kapasitas harus lebih dari 0")
        self.capacity = capacity
        self.storage = [None] * capacity

    def __len__(self):
        return self.capacity

    def __getitem__(self, position):
        if position < 0 or position >= self.capacity:
            raise IndexError("Posisi tidak tersedia")
        return self.storage[position]

    def __setitem__(self, position, value):
        if position < 0 or position >= self.capacity:
            raise IndexError("Posisi tidak tersedia")
        self.storage[position] = value

    def reset(self, value):
        """Mengganti seluruh isi array dengan nilai tertentu."""
        for i in range(self.capacity):
            self.storage[i] = value

    def __iter__(self):
        for data in self.storage:
            yield data


# ==========================
# Contoh Penggunaan
# ==========================

# Membuat array dengan ukuran 4 (beda dari teman kamu yang 5)
data_array = Array(4)

print("Total elemen dalam array:", len(data_array))

# Mengisi nilai
data_array[0] = 5
data_array[1] = 15
data_array[2] = 25
data_array[3] = 35

print("\nIsi array sekarang:")
for nilai in data_array:
    print(nilai)

# Mengambil salah satu elemen
print("\nElemen pada posisi 2:", data_array[2])

# Reset isi array menjadi 0
data_array.reset(0)

print("\nIsi array setelah reset:")
for nilai in data_array:
    print(nilai)


