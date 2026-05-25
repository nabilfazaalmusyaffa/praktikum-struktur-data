#  SOAL 1 — N-Queens (N-Ratu)
#  Algoritma  : Backtracking Rekursif
#  Bahasa     : Python 3

#  KONSEP ALGORITMA
#  ─────────────────
#  N-Queens adalah masalah klasik: tempatkan N buah ratu di
#  papan catur N×N sehingga tidak ada dua ratu yang saling
#  menyerang (se-baris, se-kolom, maupun se-diagonal).
#
#  Backtracking bekerja dengan cara:
#    1. Coba tempatkan ratu satu per satu, baris demi baris.
#    2. Jika posisi aman → lanjut ke baris berikutnya.
#    3. Jika tidak ada kolom yang aman di baris ini → mundur
#       (backtrack) ke baris sebelumnya dan coba kolom lain.
#    4. Ulangi sampai semua N baris terisi (solusi ditemukan)
#       atau semua kemungkinan habis (tidak ada solusi).
#
#  KOMPLEKSITAS
#  ─────────────
#    • Waktu  : O(N!)  — kasus terburuk mencoba semua permutasi
#    • Ruang  : O(N)   — kedalaman rekursi = N baris
# ============================================================


def is_safe(board, row, col, n):
    """
    Memeriksa apakah posisi (row, col) aman untuk meletakkan ratu.

    Pengecekan dilakukan ke tiga arah:
      1. Kolom yang sama di baris-baris sebelumnya
      2. Diagonal kiri-atas
      3. Diagonal kanan-atas

    (Baris tidak perlu dicek karena kita hanya meletakkan
     satu ratu per baris.)

    Parameter:
        board : list[int] — board[i] = kolom ratu di baris i
        row   : int       — baris yang sedang diisi
        col   : int       — kolom yang ingin dicoba
        n     : int       — ukuran papan

    Return:
        True  jika posisi aman
        False jika ada konflik
    """
    for prev_row in range(row):
        prev_col = board[prev_row]

        # Cek kolom yang sama
        if prev_col == col:
            return False

        # Cek diagonal (selisih baris == selisih kolom)
        if abs(prev_row - row) == abs(prev_col - col):
            return False

    return True


def solve_nqueens(board, row, n, solutions):
    """
    Fungsi rekursif utama untuk menyelesaikan N-Queens.

    Strategi:
      • Basis rekursi : row == n  →  semua baris sudah diisi → simpan solusi
      • Rekursi       : coba tiap kolom di baris 'row'
                        jika aman, isi board[row] lalu panggil diri sendiri
                        untuk baris berikutnya.
                        Backtrack otomatis karena nilai board[row] di-overwrite
                        pada iterasi kolom berikutnya.

    Parameter:
        board     : list[int]       — representasi posisi ratu
        row       : int             — baris yang sedang diproses
        n         : int             — ukuran papan
        solutions : list[list[int]] — kumpulan semua solusi yang ditemukan
    """
    # ── BASIS REKURSI ──────────────────────────────────────
    if row == n:
        # Semua baris terisi → simpan salinan solusi saat ini
        solutions.append(board[:])
        return

    # ── REKURSI ────────────────────────────────────────────
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col                        # Tempatkan ratu
            solve_nqueens(board, row + 1, n, solutions)  # Lanjut ke baris berikutnya
            board[row] = -1                         # Backtrack (opsional, untuk kejelasan)


def print_board(solution, n):
    """
    Menampilkan papan catur dengan simbol:
      Q = posisi ratu
      . = petak kosong
    """
    print("  " + " ".join(str(c) for c in range(n)))   # header kolom
    for row in range(n):
        queen_col = solution[row]
        baris = ""
        for col in range(n):
            baris += "Q " if col == queen_col else ". "
        print(f"{row} {baris.strip()}")


def main():
    print("=" * 50)
    print("       PROGRAM N-QUEENS (N-RATU)")
    print("       Algoritma: Backtracking Rekursif")
    print("=" * 50)

    # ── Input ──────────────────────────────────────────────
    try:
        n = int(input("\nMasukkan ukuran papan (n): "))
        if n <= 0:
            print("Ukuran papan harus bilangan positif!")
            return
    except ValueError:
        print("Input tidak valid!")
        return

    print(f"\nMencari semua solusi untuk papan {n}×{n}...\n")

    # ── Proses ─────────────────────────────────────────────
    board     = [-1] * n   # board[i] = kolom ratu di baris i; -1 = belum diisi
    solutions = []
    solve_nqueens(board, 0, n, solutions)

    # ── Output ─────────────────────────────────────────────
    if not solutions:
        print(f"❌  Tidak ada solusi untuk papan {n}×{n}.")
    else:
        total = len(solutions)
        print(f"✅  Ditemukan {total} solusi.\n")

        tampil = input(f"Tampilkan berapa solusi? (maks {total}): ")
        try:
            tampil = min(int(tampil), total)
        except ValueError:
            tampil = 1

        for i in range(tampil):
            print(f"\n{'─'*30}")
            print(f"  Solusi #{i + 1}")
            print(f"{'─'*30}")
            print_board(solutions[i], n)
            print(f"  Posisi ratu (baris → kolom): {solutions[i]}")


# ── Contoh Output ────────────────────────────────────────
# Masukkan ukuran papan (n): 4
#
# ✅  Ditemukan 2 solusi.
#
# Tampilkan berapa solusi? (maks 2): 2
#
# ──────────────────────────────
#   Solusi #1
# ──────────────────────────────
#   0 1 2 3
# 0 . Q . .
# 1 . . . Q
# 2 Q . . .
# 3 . . Q .
#   Posisi ratu (baris → kolom): [1, 3, 0, 2]
#
# ──────────────────────────────
#   Solusi #2
# ──────────────────────────────
#   0 1 2 3
# 0 . . Q .
# 1 Q . . .
# 2 . . . Q
# 3 . Q . .
#   Posisi ratu (baris → kolom): [2, 0, 3, 1]


if __name__ == "__main__":
    main()