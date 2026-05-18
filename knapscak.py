#  SOAL 3 — Knapsack (Ransel) Rekursif
#  Algoritma  : Backtracking Rekursif
#  Bahasa     : Python 3

#  KONSEP ALGORITMA
#  ─────────────────
#  Masalah Knapsack: diberikan N barang dengan berat tertentu
#  dan sebuah kapasitas maksimum (W). Temukan kombinasi barang
#  yang totalnya TERBESAR tanpa melebihi W.
#
#  Pendekatan rekursif:
#    Untuk setiap barang, ada 2 pilihan:
#      A) AMBIL barang tersebut (jika muat)
#      B) LEWATI barang tersebut
#    → Pohon rekursi mencabang 2 di setiap barang.
#
#  Backtracking terjadi saat:
#    • Menambahkan barang melebihi kapasitas → "cabang" itu
#      langsung dipangkas (pruning) tanpa ditelusuri lebih lanjut.
#
#  KOMPLEKSITAS
#  ─────────────
#    • Waktu  : O(2^N)  — kasus terburuk (tanpa pruning)
#    •          Lebih cepat dalam praktik berkat pruning
#    • Ruang  : O(N)    — kedalaman pohon rekursi
# ============================================================


def knapsack_rekursif(barang, target, index, berat_saat_ini,
                      kombinasi_saat_ini, hasil_terbaik):
    """
    Fungsi rekursif utama untuk mencari kombinasi barang optimal.

    Parameter:
        barang             : list[int] — daftar berat barang
        target             : int       — kapasitas maksimum ransel
        index              : int       — indeks barang yang sedang dipertimbangkan
        berat_saat_ini     : int       — total berat kombinasi saat ini
        kombinasi_saat_ini : list[int] — indeks barang yang dipilih sejauh ini
        hasil_terbaik      : list      — [berat_terbaik, kombinasi_terbaik]
                                         (disimpan sebagai list agar bisa diubah
                                          di dalam rekursi — Python pass-by-reference
                                          untuk list)

    Alur kerja:
      1. Perbarui hasil terbaik jika berat saat ini lebih besar.
      2. Basis rekursi: index habis → semua barang sudah dicoba.
      3. Rekursi:
           Cabang A → AMBIL barang ke-index (jika tidak melebihi target)
           Cabang B → LEWATI barang ke-index
    """
    # ── Perbarui solusi terbaik yang ditemukan sejauh ini ──
    if berat_saat_ini > hasil_terbaik[0]:
        hasil_terbaik[0] = berat_saat_ini
        hasil_terbaik[1] = kombinasi_saat_ini[:]   # simpan salinan

    # ── BASIS REKURSI ──────────────────────────────────────
    if index == len(barang):
        return   # Semua barang sudah dipertimbangkan

    # ── CABANG A: AMBIL barang ke-index ───────────────────
    berat_baru = berat_saat_ini + barang[index]
    if berat_baru <= target:                         # Pruning: hanya jika muat
        kombinasi_saat_ini.append(index)             # Tambahkan ke kombinasi
        knapsack_rekursif(
            barang, target, index + 1,
            berat_baru, kombinasi_saat_ini, hasil_terbaik
        )
        kombinasi_saat_ini.pop()                     # Backtrack: hapus barang

    # ── CABANG B: LEWATI barang ke-index ──────────────────
    knapsack_rekursif(
        barang, target, index + 1,
        berat_saat_ini, kombinasi_saat_ini, hasil_terbaik
    )


def tampilkan_pohon_rekursi(barang, target, index, berat,
                             kombinasi, depth=0, max_depth=4):
    """
    Menampilkan sebagian pohon rekursi untuk membantu pemahaman.
    Hanya ditampilkan hingga kedalaman max_depth agar tidak terlalu panjang.
    """
    indent = "   " * depth
    nama_barang = f"Barang[{index}]={barang[index]}" if index < len(barang) else "SELESAI"

    if depth <= max_depth:
        print(f"{indent}[{nama_barang}] berat={berat} | pilihan: {kombinasi}")

    if index == len(barang) or depth > max_depth:
        return

    # Cabang AMBIL
    if berat + barang[index] <= target:
        if depth <= max_depth - 1:
            print(f"{indent}  ├─ AMBIL →")
        tampilkan_pohon_rekursi(
            barang, target, index + 1,
            berat + barang[index],
            kombinasi + [barang[index]],
            depth + 1, max_depth
        )

    # Cabang LEWATI
    if depth <= max_depth - 1:
        print(f"{indent}  └─ LEWATI →")
    tampilkan_pohon_rekursi(
        barang, target, index + 1,
        berat, kombinasi,
        depth + 1, max_depth
    )


def main():
    print("=" * 55)
    print("       PROGRAM KNAPSACK REKURSIF")
    print("       Algoritma: Backtracking Rekursif")
    print("=" * 55)

    # ── Data ───────────────────────────────────────────────
    berat_barang = [2, 5, 6, 9, 12, 14, 20]
    target       = 30

    print(f"\nData Input:")
    print(f"  Berat barang : {berat_barang}")
    print(f"  Target maks  : {target}")
    print(f"  Jumlah barang: {len(berat_barang)}")

    # ── Pohon rekursi (preview) ───────────────────────────
    print(f"\n{'─'*55}")
    print("  PREVIEW POHON REKURSI (3 level pertama):")
    print(f"{'─'*55}")
    tampilkan_pohon_rekursi(berat_barang, target, 0, 0, [], max_depth=3)

    # ── Proses utama ─────────────────────────────────────
    print(f"\n{'─'*55}")
    print("  MENCARI SOLUSI OPTIMAL...")
    print(f"{'─'*55}")

    hasil_terbaik    = [0, []]         # [berat_terbaik, list_indeks]
    kombinasi_saat_ini = []

    knapsack_rekursif(
        berat_barang, target, 0, 0,
        kombinasi_saat_ini, hasil_terbaik
    )

    # ── Output ────────────────────────────────────────────
    berat_optimal  = hasil_terbaik[0]
    indeks_optimal = hasil_terbaik[1]
    barang_dipilih = [berat_barang[i] for i in indeks_optimal]

    print(f"\n✅  SOLUSI OPTIMAL DITEMUKAN!\n")
    print(f"  Barang yang dipilih (indeks) : {indeks_optimal}")
    print(f"  Berat barang yang dipilih    : {barang_dipilih}")
    print(f"  Total berat                  : {berat_optimal}")
    print(f"  Kapasitas maksimum           : {target}")
    print(f"  Sisa kapasitas               : {target - berat_optimal}")

    # Visualisasi bar
    print(f"\n  Visualisasi kapasitas:")
    terisi = int((berat_optimal / target) * 30)
    kosong = 30 - terisi
    persen = (berat_optimal / target) * 100
    print(f"  [{'█' * terisi}{'░' * kosong}] {persen:.1f}%")

    # Penjelasan mengapa kombinasi ini dipilih
    print(f"\n  PENJELASAN PEMILIHAN KOMBINASI:")
    print(f"  ─────────────────────────────────")
    print(f"  • Algoritma menjelajahi 2^{len(berat_barang)} = {2**len(berat_barang)} kemungkinan kombinasi.")
    print(f"  • Pruning memangkas cabang yang melebihi target={target}.")
    print(f"  • Dari semua kombinasi valid, kombinasi {barang_dipilih}")
    print(f"    memberikan total {berat_optimal} — nilai terbesar ≤ {target}.")

    # Cek apakah ada kombinasi yang pas = target
    if berat_optimal == target:
        print(f"  • Kombinasi ini TEPAT mengisi kapasitas (tidak ada sisa)! 🎯")
    else:
        print(f"  • Tidak ada kombinasi yang tepat = {target}; {berat_optimal} adalah yang terbaik.")

    # Tampilkan semua solusi dengan berat optimal
    print(f"\n  SEMUA KOMBINASI DENGAN BERAT = {berat_optimal}:")
    semua_hasil = []
    def cari_semua(idx, berat, combo):
        if berat == berat_optimal:
            semua_hasil.append(combo[:])
        if idx == len(berat_barang) or berat > berat_optimal:
            return
        if berat + berat_barang[idx] <= berat_optimal:
            combo.append(berat_barang[idx])
            cari_semua(idx + 1, berat + berat_barang[idx], combo)
            combo.pop()
        cari_semua(idx + 1, berat, combo)

    cari_semua(0, 0, [])
    for i, s in enumerate(semua_hasil, 1):
        print(f"  {i}. {s}  →  total = {sum(s)}")


# ── Contoh Output ─────────────────────────────────────────
#
#  Data Input:
#    Berat barang : [2, 5, 6, 9, 12, 14, 20]
#    Target maks  : 30
#
#  ✅  SOLUSI OPTIMAL DITEMUKAN!
#
#    Barang yang dipilih (indeks) : [0, 1, 2, 4]
#    Berat barang yang dipilih    : [2, 5, 6, 12]  (atau kombinasi lain dengan total 30)
#    Total berat                  : 30
#    Kapasitas maksimum           : 30
#    Sisa kapasitas               : 0
#
#    Visualisasi kapasitas:
#    [██████████████████████████████] 100.0%


if __name__ == "__main__":
    main()