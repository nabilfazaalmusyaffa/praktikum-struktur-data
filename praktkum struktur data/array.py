class Array:
    def __init__(self, size):
        """
        Konstruktor untuk membuat array dengan ukuran tetap.
        Semua elemen diisi None saat awal.
        """
        if size <= 0:
            raise ValueError("Ukuran array harus lebih dari 0")
        self._size = size
        self._data = [None] * size

    def __len__(self):
        """
        Mengembalikan panjang array.
        """
        return self._size

    def __getitem__(self, index):
        """
        Mengambil nilai pada indeks tertentu.
        """
        if not 0 <= index < self._size:
            raise IndexError("Index di luar batas")
        return self._data[index]

    def __setitem__(self, index, value):
        """
        Mengubah nilai pada indeks tertentu.
        """
        if not 0 <= index < self._size:
            raise IndexError("Index di luar batas")
        self._data[index] = value

    def clear(self, value):
        """
        Mengisi semua elemen array dengan nilai tertentu.
        """
        for i in range(self._size):
            self._data[i] = value

    def __iter__(self):
        """
        Membuat array bisa digunakan dalam perulangan.
        """
        for item in self._data:
            yield item

# Contoh penggunaan kelas Array

# Membuat array dengan ukuran 5
arr = Array(5)

print("Panjang array:", len(arr))

# Mengisi nilai
arr[0] = 10
arr[1] = 20
arr[2] = 30

print("\nIsi array setelah diisi:")
for item in arr:
    print(item)

# Mengambil nilai tertentu
print("\nNilai pada index 1:", arr[1])

# Mengosongkan array dengan nilai 0
arr.clear(0)

print("\nIsi array setelah clear:")
for item in arr:
    print(item)
