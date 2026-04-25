"""
╔══════════════════════════════════════════════════════════════════╗
║         SIMULASI QUEUE (ANTRIAN) - STRUKTUR DATA                ║
║         D4 Manajemen Informatika - Semester 2                   ║
╚══════════════════════════════════════════════════════════════════╝

Program ini mendemonstrasikan 5 kasus penggunaan Queue:
  1. Antrian Printer     (FIFO Queue)
  2. Hot Potato          (Circular Queue)
  3. Antrian Rumah Sakit (Priority Queue)
  4. BFS Graph Traversal (Queue untuk BFS)
  5. Loket Bandara       (Multi-Server Queue)
"""

import time
import heapq  # untuk priority queue (built-in, tidak perlu install)
from collections import deque  # untuk circular dan BFS queue

# ─────────────────────────────────────────────────────────────────
#  HELPER: Fungsi tampilan umum
# ─────────────────────────────────────────────────────────────────

def garis(karakter="─", panjang=60):
    """Cetak garis pemisah."""
    print(karakter * panjang)

def header_kasus(nomor, judul, jenis_queue):
    """Cetak header untuk setiap kasus."""
    print()
    garis("═")
    print(f"  KASUS {nomor}: {judul}")
    print(f"  Jenis Queue : {jenis_queue}")
    garis("═")
    time.sleep(0.5)

def tampilkan_queue(queue, label="Queue saat ini"):
    """Tampilkan isi queue secara visual."""
    if len(queue) == 0:
        print(f"  {label}: [ KOSONG ]")
    else:
        isi = " | ".join(str(item) for item in queue)
        print(f"  {label}: [ {isi} ]")
        print(f"           {'FRONT':^{max(4, len(str(queue[0])))}}{'':>{max(1,(len(isi)-len(str(queue[0])))//2)}}REAR")

def jeda(detik=0.8):
    """Jeda waktu agar output terasa seperti animasi."""
    time.sleep(detik)


# ══════════════════════════════════════════════════════════════════
#  KASUS 1: ANTRIAN PRINTER (FIFO Queue)
# ══════════════════════════════════════════════════════════════════

class AntrianPrinter:
    """
    FIFO Queue - First In, First Out.
    Dokumen yang pertama dikirim akan pertama dicetak.
    """

    def __init__(self):
        self.queue = deque()  # deque untuk efisiensi enqueue/dequeue

    def enqueue(self, dokumen):
        """Tambah dokumen ke BELAKANG antrian."""
        self.queue.append(dokumen)
        print(f"  [ENQUEUE] 📄 '{dokumen}' masuk antrian")
        tampilkan_queue(list(self.queue))
        jeda(0.7)

    def dequeue(self):
        """Ambil dokumen dari DEPAN antrian (FIFO)."""
        if not self.queue:
            print("  [INFO] Antrian kosong! Tidak ada dokumen.")
            return None
        dokumen = self.queue.popleft()
        print(f"  [DEQUEUE] 🖨️  Mencetak: '{dokumen}'  ✅ Selesai!")
        tampilkan_queue(list(self.queue))
        jeda(0.7)
        return dokumen

    def is_empty(self):
        return len(self.queue) == 0


def jalankan_printer():
    header_kasus(1, "ANTRIAN PRINTER", "FIFO (First In, First Out)")
    print("  Konsep: Dokumen dicetak sesuai urutan masuk.\n")

    printer = AntrianPrinter()
    dokumen_masuk = [
        "Laporan_Keuangan.pdf",
        "Tugas_Strukdat.docx",
        "Foto_Wisuda.jpg",
        "Sertifikat.pdf",
        "Absensi_Kelas.xlsx"
    ]

    # ── Fase 1: Semua dokumen masuk antrian ──
    garis()
    print("  FASE 1: Pengguna mengirim dokumen ke printer\n")
    for dok in dokumen_masuk:
        printer.enqueue(dok)

    # ── Fase 2: Printer memproses satu per satu ──
    garis()
    print("\n  FASE 2: Printer memproses dokumen (FIFO)\n")
    while not printer.is_empty():
        printer.dequeue()

    print("\n  ✅ Semua dokumen selesai dicetak!")
    garis()
    jeda(1)


# ══════════════════════════════════════════════════════════════════
#  KASUS 2: HOT POTATO (Circular Queue)
# ══════════════════════════════════════════════════════════════════

class HotPotato:
    """
    Circular Queue - elemen terakhir terhubung ke elemen pertama.
    Pemain melempar 'kentang panas', pemain yang memegang saat
    hitungan berhenti akan dieliminasi.
    """

    def __init__(self, nama_pemain):
        # Circular queue direpresentasikan dengan deque
        self.queue = deque(nama_pemain)

    def putar(self, hitungan):
        """
        Putar kentang sebanyak 'hitungan' kali.
        Caranya: pindahkan elemen depan ke belakang (rotasi).
        """
        for _ in range(hitungan):
            # Ambil dari depan, taruh di belakang = rotasi circular
            self.queue.append(self.queue.popleft())

    def eliminasi(self):
        """Hapus pemain yang sedang memegang kentang (posisi depan)."""
        return self.queue.popleft()

    def pemenang(self):
        return self.queue[0]

    def tampilkan(self):
        pemain = list(self.queue)
        print(f"  Lingkaran: {' → '.join(pemain)} → (kembali ke {pemain[0]})")

    def sisa_pemain(self):
        return len(self.queue)


def jalankan_hot_potato():
    header_kasus(2, "HOT POTATO", "Circular Queue")
    print("  Konsep: Pemain melempar kentang berputar.\n"
          "  Saat musik berhenti, yang pegang kentang = ELIMINATED!\n")

    pemain = ["Andi", "Budi", "Cici", "Dina", "Edo", "Fani"]
    hitungan_per_ronde = 4  # kentang dilempar 4x setiap ronde
    permainan = HotPotato(pemain)

    garis()
    print(f"  Pemain awal ({len(pemain)} orang):")
    permainan.tampilkan()
    jeda(1)

    ronde = 1
    while permainan.sisa_pemain() > 1:
        garis()
        print(f"\n  🎵 RONDE {ronde} — Musik mulai!\n")

        # Tampilkan proses perputaran kentang
        for langkah in range(1, hitungan_per_ronde + 1):
            pemegang = permainan.queue[0]
            print(f"     Lemparan {langkah}: 🥔 [{pemegang}] memegang kentang...")
            permainan.putar(1)  # putar 1 langkah
            jeda(0.4)

        print(f"\n  🛑 MUSIK BERHENTI!")
        yang_pegang = permainan.queue[0]
        print(f"  💀 [{yang_pegang}] memegang kentang → ELIMINATED!")
        permainan.eliminasi()

        print(f"\n  Sisa pemain ({permainan.sisa_pemain()} orang):")
        permainan.tampilkan()
        jeda(0.8)
        ronde += 1

    garis()
    print(f"\n  🏆 PEMENANG: [{permainan.pemenang()}] 🎉")
    garis()
    jeda(1)


# ══════════════════════════════════════════════════════════════════
#  KASUS 3: ANTRIAN RUMAH SAKIT (Priority Queue)
# ══════════════════════════════════════════════════════════════════

class AntrianRumahSakit:
    """
    Priority Queue - data dengan prioritas lebih tinggi diproses dulu.
    Prioritas 1 = paling darurat, Prioritas 3 = normal.
    Menggunakan heapq (min-heap) bawaan Python.
    """

    def __init__(self):
        self.heap = []       # min-heap: angka terkecil = prioritas tertinggi
        self.counter = 0     # tiebreaker jika prioritas sama (FIFO)

    def enqueue(self, nama, kondisi, prioritas):
        """Tambah pasien ke priority queue."""
        # Format: (prioritas, urutan_masuk, nama, kondisi)
        heapq.heappush(self.heap, (prioritas, self.counter, nama, kondisi))
        self.counter += 1

        label_prioritas = {1: "🚨 DARURAT", 2: "⚠️  SEGERA", 3: "✅ NORMAL"}
        print(f"  [ENQUEUE] {label_prioritas[prioritas]} | {nama:10} | {kondisi}")
        self._tampilkan()
        jeda(0.7)

    def dequeue(self):
        """Panggil pasien dengan prioritas tertinggi."""
        if not self.heap:
            print("  [INFO] Tidak ada pasien dalam antrian.")
            return None
        prioritas, _, nama, kondisi = heapq.heappop(self.heap)
        label = {1: "🚨 DARURAT", 2: "⚠️  SEGERA", 3: "✅ NORMAL"}[prioritas]
        print(f"  [DEQUEUE] 👨‍⚕️  Memanggil: {nama} ({label} - {kondisi})")
        self._tampilkan()
        jeda(0.7)
        return nama

    def _tampilkan(self):
        """Tampilkan isi antrian berdasar prioritas."""
        if not self.heap:
            print("  Antrian RS  : [ KOSONG ]")
            return
        # Salin dan urutkan untuk tampilan
        tampil = sorted(self.heap)
        label = {1: "🚨", 2: "⚠️ ", 3: "✅"}
        isi = " | ".join(f"{label[p[0]]}{p[2]}" for p in tampil)
        print(f"  Antrian RS  : [ {isi} ]")
        print(f"  (Urutan layanan: prioritas terkecil = paling darurat)")

    def is_empty(self):
        return len(self.heap) == 0


def jalankan_rumah_sakit():
    header_kasus(3, "ANTRIAN RUMAH SAKIT", "Priority Queue")
    print("  Konsep: Pasien paling kritis dilayani lebih dulu,\n"
          "  bukan berdasar urutan datang.\n"
          "  Prioritas: 1=Darurat  2=Segera  3=Normal\n")

    rs = AntrianRumahSakit()
    pasien = [
        ("Pak Budi",   "Cek Rutin",        3),
        ("Ibu Cici",   "Demam Tinggi",     2),
        ("Anak Dani",  "Serangan Jantung", 1),
        ("Mbak Eka",   "Patah Tangan",     2),
        ("Pak Faris",  "Kontrol Obat",     3),
        ("Ibu Gina",   "Sesak Napas",      1),
    ]

    # ── Fase 1: Pasien mendaftar ──
    garis()
    print("  FASE 1: Pasien mendaftar ke loket\n")
    for nama, kondisi, prioritas in pasien:
        rs.enqueue(nama, kondisi, prioritas)

    # ── Fase 2: Dokter memanggil pasien ──
    garis()
    print("\n  FASE 2: Dokter memanggil pasien (berdasar PRIORITAS)\n")
    urutan = 1
    while not rs.is_empty():
        print(f"  --- Pasien ke-{urutan} ---")
        rs.dequeue()
        urutan += 1

    print("\n  ✅ Semua pasien sudah dilayani!")
    garis()
    jeda(1)


# ══════════════════════════════════════════════════════════════════
#  KASUS 4: BFS - BREADTH FIRST SEARCH
# ══════════════════════════════════════════════════════════════════

def bfs_traversal(graph, mulai):
    """
    BFS menggunakan Queue.
    Menjelajahi graph per level — semua tetangga dikunjungi
    sebelum berpindah ke level berikutnya.

    graph : dictionary {node: [tetangga1, tetangga2, ...]}
    mulai : node awal
    """

    # Queue untuk BFS (deque = efisien untuk popleft)
    queue = deque()
    dikunjungi = set()
    urutan_kunjungan = []
    level_node = {mulai: 0}

    # ── Langkah awal: masukkan node pertama ──
    queue.append(mulai)
    dikunjungi.add(mulai)

    print(f"  Start → Node '{mulai}' masuk queue\n")
    jeda(0.5)

    langkah = 1

    while queue:
        garis("─", 55)
        # Tampilkan isi queue sebelum dequeue
        print(f"  Langkah {langkah}:")
        print(f"  Queue      : {list(queue)}")

        # DEQUEUE: ambil node terdepan
        node_sekarang = queue.popleft()
        urutan_kunjungan.append(node_sekarang)
        level = level_node[node_sekarang]

        print(f"  [DEQUEUE]  : Kunjungi Node '{node_sekarang}' (Level {level})")

        # Cek semua tetangga
        tetangga_baru = []
        for tetangga in graph.get(node_sekarang, []):
            if tetangga not in dikunjungi:
                dikunjungi.add(tetangga)
                queue.append(tetangga)        # ENQUEUE tetangga
                level_node[tetangga] = level + 1
                tetangga_baru.append(tetangga)

        if tetangga_baru:
            print(f"  [ENQUEUE]  : Tetangga baru masuk queue: {tetangga_baru}")
        else:
            print(f"  [INFO]     : Tidak ada tetangga baru")

        print(f"  Sudah dikunjungi: {urutan_kunjungan}")
        jeda(0.9)
        langkah += 1

    return urutan_kunjungan


def jalankan_bfs():
    header_kasus(4, "BFS - BREADTH FIRST SEARCH", "FIFO Queue untuk Traversal Graph")
    print("  Konsep: Jelajahi graph per 'level'.\n"
          "  Kunjungi semua tetangga terdekat dulu,\n"
          "  baru lanjut ke yang lebih jauh.\n")

    # Graph sederhana (seperti peta kota)
    #
    #      A
    #    /   \
    #   B     C
    #  / \   / \
    # D   E F   G
    #      \ |
    #        H

    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F", "G"],
        "D": ["B"],
        "E": ["B", "H"],
        "F": ["C", "H"],
        "G": ["C"],
        "H": ["E", "F"]
    }

    print("  Struktur Graph:")
    print("        A")
    print("      /   \\")
    print("     B     C")
    print("    / \\   / \\")
    print("   D   E F   G")
    print("        \\ |")
    print("         H")
    print()
    garis()
    print("\n  Mulai BFS dari Node 'A'\n")
    jeda(0.8)

    hasil = bfs_traversal(graph, "A")

    garis()
    print(f"\n  ✅ BFS Selesai!")
    print(f"  Urutan kunjungan : {' → '.join(hasil)}")
    print(f"  Total node       : {len(hasil)}")
    garis()
    jeda(1)


# ══════════════════════════════════════════════════════════════════
#  KASUS 5: LOKET BANDARA (Multi-Server Queue)
# ══════════════════════════════════════════════════════════════════

class LoketBandara:
    """
    Simulasi antrian bandara dengan beberapa loket.
    Satu antrian umum → penumpang diarahkan ke loket yang kosong.
    """

    def __init__(self, jumlah_loket=2):
        self.antrian = deque()          # antrian penumpang
        self.jumlah_loket = jumlah_loket
        # Status tiap loket: None = kosong, nama = sedang melayani
        self.loket = {f"Loket {i+1}": None for i in range(jumlah_loket)}
        self.total_dilayani = 0

    def enqueue(self, penumpang):
        """Penumpang bergabung ke antrian."""
        self.antrian.append(penumpang)
        print(f"  [ENQUEUE] 🧍 '{penumpang}' bergabung ke antrian")
        self._tampilkan_status()
        jeda(0.5)

    def dequeue_ke_loket(self):
        """Arahkan penumpang terdepan ke loket yang kosong."""
        # Cari loket kosong
        loket_kosong = None
        for nama_loket, isi in self.loket.items():
            if isi is None:
                loket_kosong = nama_loket
                break

        if loket_kosong is None:
            print("  [INFO] Semua loket sedang sibuk. Penumpang menunggu...")
            return False

        if not self.antrian:
            print("  [INFO] Antrian kosong!")
            return False

        # DEQUEUE: ambil dari depan antrian
        penumpang = self.antrian.popleft()
        self.loket[loket_kosong] = penumpang
        self.total_dilayani += 1

        print(f"  [DEQUEUE] ✈️  '{penumpang}' → diarahkan ke {loket_kosong}")
        self._tampilkan_status()
        jeda(0.6)
        return True

    def selesaikan_loket(self, nama_loket):
        """Penumpang selesai dilayani, loket kembali kosong."""
        penumpang = self.loket[nama_loket]
        if penumpang:
            print(f"  [SELESAI] ✅ {nama_loket}: '{penumpang}' check-in selesai → Loket kosong")
            self.loket[nama_loket] = None
            self._tampilkan_status()
            jeda(0.5)

    def _tampilkan_status(self):
        """Tampilkan status antrian dan loket."""
        # Antrian
        if self.antrian:
            isi = " | ".join(list(self.antrian))
            print(f"  Antrian    : [ {isi} ]  ({len(self.antrian)} orang)")
        else:
            print(f"  Antrian    : [ KOSONG ]")

        # Status loket
        status_loket = []
        for nama, isi in self.loket.items():
            if isi:
                status_loket.append(f"{nama}: 🔴 {isi}")
            else:
                status_loket.append(f"{nama}: 🟢 KOSONG")
        print(f"  Loket      : {' | '.join(status_loket)}")

    def is_semua_selesai(self):
        """Cek apakah antrian kosong dan semua loket kosong."""
        return (len(self.antrian) == 0 and
                all(v is None for v in self.loket.values()))


def jalankan_bandara():
    header_kasus(5, "SIMULASI LOKET BANDARA", "Multi-Server FIFO Queue")
    print("  Konsep: Satu antrian umum melayani beberapa loket.\n"
          "  Penumpang terdepan diarahkan ke loket yang kosong.\n"
          "  Jika semua loket sibuk, penumpang menunggu di antrian.\n")

    bandara = LoketBandara(jumlah_loket=2)

    penumpang_datang = [
        "Andi (Jakarta)",
        "Bela (Surabaya)",
        "Coco (Bali)",
        "Dita (Medan)",
        "Evan (Makassar)",
        "Fika (Yogya)",
    ]

    # ── Fase 1: Penumpang berdatangan ──
    garis()
    print("  FASE 1: Penumpang berdatangan & antri\n")
    for p in penumpang_datang[:4]:  # 4 penumpang masuk dulu
        bandara.enqueue(p)

    # ── Fase 2: Loket mulai melayani ──
    garis()
    print("\n  FASE 2: Loket mulai melayani\n")

    # Loket 1 dan 2 melayani 2 penumpang pertama
    bandara.dequeue_ke_loket()  # Penumpang 1 → Loket 1
    bandara.dequeue_ke_loket()  # Penumpang 2 → Loket 2

    # ── Fase 3: Penumpang baru datang, loket 1 selesai ──
    garis()
    print("\n  FASE 3: Penumpang baru datang, Loket 1 selesai\n")
    for p in penumpang_datang[4:]:  # 2 penumpang tambahan
        bandara.enqueue(p)
    bandara.selesaikan_loket("Loket 1")  # Loket 1 kosong
    bandara.dequeue_ke_loket()            # Loket 1 langsung layani berikutnya

    # ── Fase 4: Selesaikan semua ──
    garis()
    print("\n  FASE 4: Melayani sisa antrian\n")
    bandara.selesaikan_loket("Loket 2")
    while not bandara.is_semua_selesai():
        bandara.dequeue_ke_loket()
        jeda(0.3)
        # Selesaikan loket yang sedang aktif
        for nama_loket, isi in list(bandara.loket.items()):
            if isi:
                bandara.selesaikan_loket(nama_loket)

    garis()
    print(f"\n  ✅ Semua penumpang selesai check-in!")
    print(f"  Total dilayani: {bandara.total_dilayani} penumpang")
    garis()
    jeda(1)


# ══════════════════════════════════════════════════════════════════
#  MENU UTAMA
# ══════════════════════════════════════════════════════════════════

def tampilkan_menu():
    """Tampilkan menu pilihan kasus."""
    print()
    garis("═")
    print("  SIMULASI QUEUE - STRUKTUR DATA")
    print("  D4 Manajemen Informatika")
    garis("═")
    print("  Pilih kasus yang ingin disimulasikan:\n")
    print("  [1] Antrian Printer     (FIFO Queue)")
    print("  [2] Hot Potato          (Circular Queue)")
    print("  [3] Antrian Rumah Sakit (Priority Queue)")
    print("  [4] BFS Graph Traversal (Queue untuk BFS)")
    print("  [5] Loket Bandara       (Multi-Server Queue)")
    print("  [6] Jalankan SEMUA kasus")
    print("  [0] Keluar")
    garis()


def main():
    """Fungsi utama — menu interaktif."""
    daftar_kasus = {
        "1": jalankan_printer,
        "2": jalankan_hot_potato,
        "3": jalankan_rumah_sakit,
        "4": jalankan_bfs,
        "5": jalankan_bandara,
    }

    while True:
        tampilkan_menu()
        pilihan = input("  Masukkan pilihan (0-6): ").strip()

        if pilihan == "0":
            print("\n  Terima kasih! Program selesai. 👋\n")
            break
        elif pilihan in daftar_kasus:
            daftar_kasus[pilihan]()
            input("\n  [Tekan ENTER untuk kembali ke menu...]")
        elif pilihan == "6":
            print("\n  Menjalankan semua kasus...\n")
            jeda(0.5)
            for fn in daftar_kasus.values():
                fn()
            print("\n  ✅ Semua kasus selesai dijalankan!\n")
            input("  [Tekan ENTER untuk kembali ke menu...]")
        else:
            print("  ⚠️  Pilihan tidak valid. Coba lagi.\n")


# ── Entry point ──
if __name__ == "__main__":
    main()