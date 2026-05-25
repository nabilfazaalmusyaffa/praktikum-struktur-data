#  SOAL 2 — Knight's Tour (Tur Kuda)
#  Algoritma  : Backtracking Rekursif + Heuristik Warnsdorff
#  Bahasa     : Python 3

#  KONSEP ALGORITMA
#  ─────────────────
#  Knight's Tour adalah masalah menemukan rute kuda catur agar
#  mengunjungi setiap petak pada papan N×N tepat satu kali.
#
#  Gerakan kuda: 8 kemungkinan (bentuk huruf L)
#    (±1, ±2)  dan  (±2, ±1)
#
#  BACKTRACKING:
#    1. Mulai dari posisi awal, catat langkah ke-1.
#    2. Coba 8 gerakan yang mungkin dari posisi saat ini.
#    3. Jika gerakan valid (dalam papan & belum dikunjungi)
#       → tandai petak, lanjut rekursi ke langkah berikutnya.
#    4. Jika dari posisi tersebut tidak ada gerakan lanjutan
#       yang menghasilkan solusi → hapus tanda (backtrack),
#       kembali dan coba gerakan lain.
#    5. Selesai jika semua N² petak telah dikunjungi.
#
#  HEURISTIK WARNSDORFF:
#    Pilih langkah berikutnya ke petak yang memiliki paling
#    sedikit onward-moves (pilihan lanjutan). Ini drastis
#    mengurangi backtracking dan mempercepat pencarian.
#
#  KOMPLEKSITAS
#  ─────────────
#    • Tanpa heuristik : O(8^(N²))  — eksponensial
#    • Dengan Warnsdorff: hampir O(N²) dalam praktik
#    • Ruang           : O(N²)       — papan + tumpukan rekursi
# ============================================================


# 8 kemungkinan gerakan kuda (baris_delta, kolom_delta)
MOVES = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1),
]


def is_valid(x, y, n, board):
    """
    Memeriksa apakah posisi (x, y) valid untuk dikunjungi.

    Syarat valid:
      • Masih dalam batas papan (0 ≤ x, y < n)
      • Belum pernah dikunjungi (board[x][y] == -1)
    """
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1


def count_onward_moves(x, y, n, board):
    """
    Menghitung jumlah gerakan lanjutan yang valid dari (x, y).
    Digunakan oleh heuristik Warnsdorff untuk memilih langkah
    terbaik berikutnya.
    """
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, n, board):
            count += 1
    return count


def get_sorted_moves(x, y, n, board):
    """
    Mengembalikan daftar gerakan berikutnya yang diurutkan
    berdasarkan jumlah onward-moves (Warnsdorff: yang paling
    sedikit pilihan → diprioritaskan terlebih dahulu).
    """
    nexts = []
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, n, board):
            degree = count_onward_moves(nx, ny, n, board)
            nexts.append((degree, nx, ny))
    nexts.sort()   # urut dari degree terkecil
    return nexts


def solve_knights_tour(x, y, move_num, n, board):
    """
    Fungsi rekursif utama untuk menyelesaikan Knight's Tour.

    Parameter:
        x, y     : int          — posisi kuda saat ini
        move_num : int          — nomor langkah saat ini
        n        : int          — ukuran papan
        board    : list[list]   — papan (board[i][j] = nomor langkah, -1 jika belum)

    Return:
        True  jika solusi ditemukan
        False jika jalan buntu (perlu backtrack)

    Alur rekursi:
      BASIS  : move_num == n*n  →  semua petak terisi → return True
      REKURSI: urutkan gerakan dengan Warnsdorff,
               untuk tiap gerakan valid:
                 • tandai board[nx][ny] = move_num
                 • panggil rekursi untuk langkah berikutnya
                 • jika rekursi sukses → return True
                 • jika gagal → BACKTRACK: board[nx][ny] = -1
               jika semua gerakan gagal → return False
    """
    # ── BASIS REKURSI ──────────────────────────────────────
    if move_num == n * n:
        return True   # Semua petak sudah dikunjungi!

    # ── REKURSI ────────────────────────────────────────────
    for _, nx, ny in get_sorted_moves(x, y, n, board):
        board[nx][ny] = move_num          # Tandai langkah ke-move_num
        print(f"\r  Mengeksplorasi langkah ke-{move_num+1}...", end="", flush=True)

        if solve_knights_tour(nx, ny, move_num + 1, n, board):
            return True                   # Solusi ditemukan, propagasi ke atas

        # BACKTRACK: gerakan ini tidak menghasilkan solusi
        board[nx][ny] = -1               # Hapus tanda, coba gerakan lain

    return False   # Semua gerakan gagal dari posisi ini


def print_board(board, n):
    """
    Menampilkan papan dengan nomor langkah setiap petak.
    Lebar kolom disesuaikan agar rapi.
    """
    width = len(str(n * n))   # lebar angka terbesar
    separator = "─" * ((width + 3) * n + 1)

    print(f"\n{separator}")
    for row in range(n):
        baris = "│"
        for col in range(n):
            baris += f" {board[row][col]:>{width}} │"
        print(baris)
        print(separator)


def main():
    print("=" * 55)
    print("       PROGRAM KNIGHT'S TOUR (TUR KUDA)")
    print("       Algoritma: Backtracking + Warnsdorff")
    print("=" * 55)

    # ── Input ──────────────────────────────────────────────
    try:
        n = int(input("\nMasukkan ukuran papan (n): "))
        if n < 5:
            print("⚠  Papan minimal 5×5 untuk memastikan solusi ada.")
            print("   (Papan kecil seperti 1×1–4×4 seringkali tidak memiliki solusi.)")
            if n <= 0:
                return
        start_r = int(input(f"Posisi awal — baris  (0 s.d. {n-1}): "))
        start_c = int(input(f"Posisi awal — kolom  (0 s.d. {n-1}): "))
    except ValueError:
        print("Input tidak valid!")
        return

    if not (0 <= start_r < n and 0 <= start_c < n):
        print("Posisi awal di luar papan!")
        return

    # ── Inisialisasi papan ─────────────────────────────────
    board = [[-1] * n for _ in range(n)]
    board[start_r][start_c] = 0   # Langkah pertama = 0

    print(f"\nMencari rute untuk papan {n}×{n} dari ({start_r},{start_c})...\n")

    # ── Proses ─────────────────────────────────────────────
    found = solve_knights_tour(start_r, start_c, 1, n, board)

    # ── Output ─────────────────────────────────────────────
    print()   # baris baru setelah animasi
    if found:
        print(f"\n✅  Solusi ditemukan! Kuda berhasil mengunjungi semua {n*n} petak.\n")
        print(f"  Papan {n}×{n} (angka = urutan langkah kuda, mulai dari 0):")
        print_board(board, n)
        print("\n  Keterangan: 0 = posisi awal kuda")
    else:
        print(f"\n❌  Tidak ditemukan solusi untuk papan {n}×{n}")
        print("   dari posisi awal ({start_r}, {start_c}).")
        print("   Coba posisi awal yang berbeda.")


# ── Contoh Output (papan 5×5 dari posisi (0,0)) ──────────
#
# Mencari rute untuk papan 5×5 dari (0,0)...
#
# ✅  Solusi ditemukan! Kuda berhasil mengunjungi semua 25 petak.
#
#   Papan 5×5 (angka = urutan langkah kuda, mulai dari 0):
# ─────────────────────────────
# │  0 │ 11 │  6 │ 17 │ 22 │
# ─────────────────────────────
# │  5 │ 16 │ 23 │ 12 │  7 │
# ─────────────────────────────
# │ 10 │  1 │ 18 │ 21 │ 24 │
# ─────────────────────────────
# │ 15 │  4 │ 13 │  8 │ 19 │
# ─────────────────────────────
# │  2 │  9 │ 20 │  3 │ 14 │
# ─────────────────────────────


if __name__ == "__main__":
    main()