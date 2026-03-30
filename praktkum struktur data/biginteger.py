class Node:
    """Class ini merepresentasikan satu kotak (node) dalam Linked List yang menyimpan satu digit."""
    def __init__(self, data):
        self.data = data    # Menyimpan nilai digit (integer)
        self.next = None    # Penunjuk (pointer) ke node/digit berikutnya

class BigInteger:
    """Class utama untuk Big Integer ADT menggunakan Singly Linked List."""
    
    def __init__(self, initValue="0"):
        """
        Inisialisasi BigInteger dari sebuah string.
        Setiap digit dari string akan disimpan ke dalam node terpisah[cite: 25].
        """
        self.head = None
        
        # Kita perlu memproses string dari belakang (digit paling kanan/satuan) 
        # karena node harus diurutkan dari least-significant digit.
        # Contoh: "45839" akan diproses sebagai '9', lalu '3', '8', '5', '4'.
        
        tail = None
        for char_digit in reversed(initValue):
            angka = int(char_digit)
            node_baru = Node(angka)
            
            # Jika linked list masih kosong, jadikan node_baru sebagai head
            if self.head is None:
                self.head = node_baru
                tail = node_baru
            else:
                # Jika sudah ada isinya, sambungkan node_baru ke belakang tail
                tail.next = node_baru
                tail = node_baru

    def toString(self):
        """Mengembalikan nilai BigInteger ke dalam bentuk string untuk ditampilkan[cite: 11]."""
        curr = self.head
        kumpulan_digit = []
        
        # Menyusuri linked list dari head sampai ujung
        while curr is not None:
            kumpulan_digit.append(str(curr.data))
            curr = curr.next
            
        # Karena di dalam linked list disimpannya terbalik (satuan di depan),
        # maka saat dijadikan string utuh, urutannya harus kita balik lagi (reversed).
        return "".join(reversed(kumpulan_digit))

    # ==========================================================
    # KERANGKA METHOD LAIN YANG HARUS KAMU LANJUTKAN SENDIRI NANTI
    # ==========================================================
    
    def __eq__(self, other):
        """Fungsi untuk membandingkan == [cite: 12, 13]"""
        pass
        
    def __lt__(self, other):
        """Fungsi untuk membandingkan < [cite: 12, 13]"""
        pass

    def __add__(self, rhsInt):
        """Fungsi untuk operator penjumlahan + [cite: 14, 16]"""
        pass
        
    def __mul__(self, rhsInt):
        """Fungsi untuk operator perkalian * [cite: 14, 17]"""
        pass

# ==========================================================
# CONTOH CARA MENGGUNAKANNYA:
# ==========================================================
if __name__ == "__main__":
    # Membuat objek BigInteger dengan nilai "45839"
    angka_besar = BigInteger("45839")
    
    # Mari kita cek apakah Head-nya benar angka 9
    print("Nilai Head:", angka_besar.head.data)
    
    # Mari kita cek apakah Node setelahnya adalah 3
    print("Nilai setelah Head:", angka_besar.head.next.data)
    
    # Tes fungsi toString()
    print("Hasil toString():", angka_besar.toString())