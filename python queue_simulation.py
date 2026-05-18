#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        SIMULASI QUEUE — GUI APLIKASI DESKTOP                ║
║        D4 Manajemen Informatika  |  Semester 2              ║
╠══════════════════════════════════════════════════════════════╣
║  Cara Menjalankan:                                          ║
║    python queue_gui.py                                      ║
║                                                              ║
║  Requirement:                                               ║
║    Python 3.x  +  Tkinter (sudah built-in di Python)        ║
║    Jika belum ada: pip install tk                           ║
╚══════════════════════════════════════════════════════════════╝

5 Simulasi Queue yang tersedia:
  1. Antrian Printer      → FIFO Queue
  2. Hot Potato           → Circular Queue
  3. Antrian Rumah Sakit  → Priority Queue
  4. BFS Traversal        → Queue untuk Graph
  5. Loket Bandara        → Multi-Server Queue
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import heapq
from collections import deque
import time


# ══════════════════════════════════════════════════════════════
#  PALET WARNA & KONSTANTA DESAIN
# ══════════════════════════════════════════════════════════════

WARNA = {
    # Background
    "bg_utama"      : "#0F172A",   # navy gelap
    "bg_panel"      : "#1E293B",   # panel sedikit terang
    "bg_sidebar"    : "#1E293B",   # sidebar
    "bg_card"       : "#334155",   # card/box queue
    "bg_header"     : "#0F172A",

    # Accent & Status
    "enqueue"       : "#22C55E",   # hijau (data masuk)
    "dequeue"       : "#EF4444",   # merah (data keluar)
    "aktif"         : "#F59E0B",   # kuning (sedang diproses)
    "normal"        : "#3B82F6",   # biru (item biasa)
    "selesai"       : "#6B7280",   # abu (sudah diproses)
    "highlight"     : "#8B5CF6",   # ungu (highlight BFS)

    # Text
    "teks_utama"    : "#F1F5F9",
    "teks_sekunder" : "#94A3B8",
    "teks_label"    : "#CBD5E1",

    # Tombol
    "btn_enqueue"   : "#16A34A",
    "btn_dequeue"   : "#DC2626",
    "btn_start"     : "#2563EB",
    "btn_reset"     : "#475569",
    "btn_hover"     : "#1D4ED8",

    # Prioritas Rumah Sakit
    "prio1"         : "#EF4444",   # darurat
    "prio2"         : "#F59E0B",   # segera
    "prio3"         : "#22C55E",   # normal

    # Loket
    "loket_kosong"  : "#22C55E",
    "loket_sibuk"   : "#F59E0B",
}

FONT = {
    "judul"     : ("Segoe UI", 18, "bold"),
    "sub_judul" : ("Segoe UI", 13, "bold"),
    "normal"    : ("Segoe UI", 11),
    "kecil"     : ("Segoe UI", 9),
    "mono"      : ("Courier New", 10),
    "box"       : ("Segoe UI", 10, "bold"),
    "sidebar"   : ("Segoe UI", 11),
}

LEBAR_APP  = 1100
TINGGI_APP = 700
DELAY_ANIM = 600   # ms — ubah angka ini untuk perlambat/percepat animasi


# ══════════════════════════════════════════════════════════════
#  KOMPONEN UI REUSABLE
# ══════════════════════════════════════════════════════════════

class TombolModern(tk.Button):
    """Tombol dengan desain modern dan efek hover."""
    def __init__(self, parent, teks, warna_bg, perintah, lebar=14, **kwargs):
        super().__init__(
            parent,
            text       = teks,
            command    = perintah,
            bg         = warna_bg,
            fg         = WARNA["teks_utama"],
            font       = FONT["normal"],
            relief     = "flat",
            cursor     = "hand2",
            padx       = 14,
            pady       = 8,
            width      = lebar,
            **kwargs
        )
        self._warna_asli = warna_bg
        self._warna_hover = self._buat_hover(warna_bg)
        self.bind("<Enter>", lambda e: self.config(bg=self._warna_hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._warna_asli))

    def _buat_hover(self, hex_color):
        """Buat warna sedikit lebih terang untuk efek hover."""
        r = min(255, int(hex_color[1:3], 16) + 25)
        g = min(255, int(hex_color[3:5], 16) + 25)
        b = min(255, int(hex_color[5:7], 16) + 25)
        return f"#{r:02X}{g:02X}{b:02X}"


class LabelStatus(tk.Label):
    """Label untuk menampilkan status / log animasi."""
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg    = WARNA["bg_panel"],
            fg    = WARNA["teks_sekunder"],
            font  = FONT["normal"],
            anchor= "w",
            pady  = 6,
            padx  = 10,
            **kwargs
        )

    def set(self, pesan, warna=None):
        self.config(text=f"  ▶  {pesan}", fg=warna or WARNA["teks_sekunder"])


class BoxQueue(tk.Canvas):
    """
    Canvas untuk menggambar kotak-kotak antrian secara visual.
    Setiap item ditampilkan sebagai card berwarna.
    """
    LEBAR_BOX  = 110
    TINGGI_BOX = 64
    GAP        = 10
    RADIUS     = 10

    def __init__(self, parent, tinggi=100, **kwargs):
        super().__init__(
            parent,
            bg      = WARNA["bg_panel"],
            height  = tinggi,
            highlightthickness = 0,
            **kwargs
        )

    def gambar_queue(self, items, warna_items=None, label_bawah=""):
        """
        Gambar ulang semua item queue sebagai box horizontal.
        items       : list string yang ditampilkan
        warna_items : dict {index: warna_hex} untuk warna khusus per item
        label_bawah : label teks di bawah canvas
        """
        self.delete("all")
        if not items:
            self.create_text(
                self.winfo_width() // 2 or 400, 50,
                text   = "[ Queue Kosong ]",
                fill   = WARNA["teks_sekunder"],
                font   = FONT["normal"]
            )
            return

        warna_items = warna_items or {}
        total_lebar = len(items) * (self.LEBAR_BOX + self.GAP) - self.GAP
        start_x     = max(10, (self.winfo_width() - total_lebar) // 2)
        if start_x < 10:
            start_x = 10

        for i, item in enumerate(items):
            x1 = start_x + i * (self.LEBAR_BOX + self.GAP)
            y1 = 15
            x2 = x1 + self.LEBAR_BOX
            y2 = y1 + self.TINGGI_BOX

            warna = warna_items.get(i, WARNA["normal"])
            self._gambar_rounded_rect(x1, y1, x2, y2, self.RADIUS, warna)

            # Teks item
            teks_item = str(item)
            if len(teks_item) > 12:
                teks_item = teks_item[:11] + "…"
            self.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2 - 6,
                text = teks_item,
                fill = "#FFFFFF",
                font = FONT["box"]
            )

            # Label nomor urut
            self.create_text(
                (x1 + x2) // 2, y2 - 10,
                text = f"#{i+1}",
                fill = "#AAAACC",
                font = FONT["kecil"]
            )

            # Label FRONT / REAR
            if i == 0:
                self._gambar_label_panah(x1, y2, "FRONT", "#94A3B8")
            if i == len(items) - 1:
                self._gambar_label_panah(x2, y2, "REAR", "#94A3B8")

        # Tanda panah antar box
        for i in range(len(items) - 1):
            x_panah = start_x + (i + 1) * (self.LEBAR_BOX + self.GAP) - self.GAP // 2 - 4
            y_panah = 15 + self.TINGGI_BOX // 2
            self.create_text(x_panah, y_panah, text="→", fill=WARNA["teks_sekunder"], font=("Segoe UI", 14))

    def _gambar_rounded_rect(self, x1, y1, x2, y2, r, warna):
        """Gambar rectangle dengan sudut membulat."""
        self.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  fill=warna, outline=warna)
        self.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  fill=warna, outline=warna)
        self.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  fill=warna, outline=warna)
        self.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  fill=warna, outline=warna)
        self.create_rectangle(x1+r, y1,     x2-r, y2,     fill=warna, outline=warna)
        self.create_rectangle(x1,   y1+r,   x2,   y2-r,   fill=warna, outline=warna)

    def _gambar_label_panah(self, x, y, teks, warna):
        self.create_text(x, y + 14, text="↑", fill=warna, font=("Segoe UI", 10))
        self.create_text(x, y + 26, text=teks, fill=warna, font=FONT["kecil"])


# ══════════════════════════════════════════════════════════════
#  KASUS 1 — ANTRIAN PRINTER (FIFO)
# ══════════════════════════════════════════════════════════════

class PanelPrinter(tk.Frame):
    """Panel simulasi antrian printer dengan FIFO Queue."""

    DOKUMEN_CONTOH = [
        "📄 Laporan.pdf", "📊 Data.xlsx", "📝 Tugas.docx",
        "🖼️ Foto.jpg", "📋 Absensi.pdf", "📑 Sertif.pdf",
    ]

    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_panel"])
        self._queue       = deque()
        self._warna_item  = {}
        self._sedang_anim = False
        self._dok_counter = 0
        self._buat_ui()

    def _buat_ui(self):
        # ── Judul ──
        tk.Label(self, text="🖨️  Antrian Printer — FIFO Queue",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_utama"],
                 font=FONT["sub_judul"]).pack(anchor="w", padx=20, pady=(16, 4))

        tk.Label(self, text="Dokumen dicetak sesuai urutan masuk (First In, First Out).",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"]).pack(anchor="w", padx=20, pady=(0, 12))

        # ── Visualisasi Queue ──
        tk.Label(self, text="  Antrian Dokumen:", bg=WARNA["bg_panel"],
                 fg=WARNA["teks_label"], font=FONT["normal"]).pack(anchor="w", padx=20)

        self.canvas_queue = BoxQueue(self, tinggi=130)
        self.canvas_queue.pack(fill="x", padx=20, pady=(4, 0))

        # ── Area Printer ──
        frame_printer = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_printer.pack(fill="x", padx=20, pady=12)

        tk.Label(frame_printer, text="Printer:", bg=WARNA["bg_panel"],
                 fg=WARNA["teks_label"], font=FONT["normal"]).pack(side="left")

        self.lbl_printer = tk.Label(
            frame_printer,
            text="[ Idle — menunggu dokumen ]",
            bg=WARNA["bg_card"], fg=WARNA["teks_sekunder"],
            font=FONT["mono"], padx=16, pady=8, relief="flat"
        )
        self.lbl_printer.pack(side="left", padx=12)

        # ── Log Status ──
        self.lbl_status = LabelStatus(self, text="  Tambahkan dokumen lalu tekan Enqueue.")
        self.lbl_status.pack(fill="x", padx=20, pady=(0, 8))

        # ── Kontrol ──
        frame_kontrol = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_kontrol.pack(padx=20, pady=8)

        self.entry_dok = tk.Entry(
            frame_kontrol, width=20, font=FONT["normal"],
            bg=WARNA["bg_card"], fg=WARNA["teks_utama"],
            insertbackground=WARNA["teks_utama"], relief="flat", bd=6
        )
        self.entry_dok.insert(0, self.DOKUMEN_CONTOH[0])
        self.entry_dok.pack(side="left", padx=(0, 8), ipady=4)

        TombolModern(frame_kontrol, "📥 Enqueue", WARNA["btn_enqueue"],
                     self._enqueue).pack(side="left", padx=4)
        TombolModern(frame_kontrol, "📤 Dequeue", WARNA["btn_dequeue"],
                     self._dequeue).pack(side="left", padx=4)
        TombolModern(frame_kontrol, "▶ Simulasi", WARNA["btn_start"],
                     self._simulasi_otomatis, lebar=12).pack(side="left", padx=4)
        TombolModern(frame_kontrol, "↺ Reset", WARNA["btn_reset"],
                     self._reset, lebar=8).pack(side="left", padx=4)

        # ── Legenda ──
        self._buat_legenda()
        # Queue awal
        self._isi_queue_awal()

    def _buat_legenda(self):
        f = tk.Frame(self, bg=WARNA["bg_panel"])
        f.pack(anchor="w", padx=20, pady=(4, 0))
        for warna, label in [
            (WARNA["enqueue"], "Baru masuk"),
            (WARNA["aktif"],   "Sedang diproses"),
            (WARNA["selesai"], "Selesai"),
            (WARNA["normal"],  "Dalam antrian"),
        ]:
            tk.Label(f, text="■", bg=WARNA["bg_panel"], fg=warna, font=("Segoe UI", 14)).pack(side="left")
            tk.Label(f, text=label + "   ", bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                     font=FONT["kecil"]).pack(side="left")

    def _isi_queue_awal(self):
        for dok in self.DOKUMEN_CONTOH[:3]:
            self._queue.append(dok)
        self._refresh_canvas()

    def _refresh_canvas(self):
        """Perbarui canvas queue dengan warna tiap item."""
        self.canvas_queue.gambar_queue(list(self._queue), self._warna_item)

    def _enqueue(self):
        if self._sedang_anim:
            return
        teks = self.entry_dok.get().strip()
        if not teks:
            messagebox.showwarning("Input Kosong", "Masukkan nama dokumen terlebih dahulu!")
            return
        self._queue.append(teks)
        idx = len(self._queue) - 1
        # Warna hijau (enqueue), lalu berubah ke biru setelah 700ms
        self._warna_item[idx] = WARNA["enqueue"]
        self._refresh_canvas()
        self.lbl_status.set(f"ENQUEUE: '{teks}' masuk ke posisi #{len(self._queue)}", WARNA["enqueue"])
        self.after(700, lambda: self._normalkan_warna(idx))
        # Auto-suggest dokumen berikutnya
        self._dok_counter = (self._dok_counter + 1) % len(self.DOKUMEN_CONTOH)
        self.entry_dok.delete(0, "end")
        self.entry_dok.insert(0, self.DOKUMEN_CONTOH[self._dok_counter])

    def _normalkan_warna(self, idx):
        if idx in self._warna_item:
            self._warna_item[idx] = WARNA["normal"]
        # Rebuild index setelah dequeue menggeser posisi
        items = list(self._queue)
        new_warna = {i: self._warna_item.get(i, WARNA["normal"]) for i in range(len(items))}
        self._warna_item = new_warna
        self._refresh_canvas()

    def _dequeue(self):
        if self._sedang_anim:
            return
        if not self._queue:
            self.lbl_status.set("Queue kosong! Tidak ada dokumen.", WARNA["dequeue"])
            return
        self._sedang_anim = True
        # Highlight merah item terdepan
        self._warna_item[0] = WARNA["aktif"]
        self._refresh_canvas()
        self.lbl_status.set("Mencetak dokumen...", WARNA["aktif"])
        self.after(DELAY_ANIM, self._selesai_dequeue)

    def _selesai_dequeue(self):
        if not self._queue:
            self._sedang_anim = False
            return
        item = self._queue.popleft()
        # Rebuild warna setelah pop
        self._warna_item = {i: self._warna_item.get(i+1, WARNA["normal"]) for i in range(len(self._queue))}
        self._refresh_canvas()
        self.lbl_printer.config(
            text=f"✅  Selesai mencetak: {item}",
            fg=WARNA["enqueue"]
        )
        self.lbl_status.set(f"DEQUEUE: '{item}' selesai dicetak!", WARNA["enqueue"])
        self._sedang_anim = False

    def _simulasi_otomatis(self):
        """Dequeue semua item satu per satu secara otomatis."""
        if self._sedang_anim or not self._queue:
            return
        self._dequeue()
        if self._queue:
            self.after(DELAY_ANIM * 2, self._simulasi_otomatis)

    def _reset(self):
        self._queue.clear()
        self._warna_item.clear()
        self._sedang_anim = False
        self._refresh_canvas()
        self.lbl_printer.config(text="[ Idle — menunggu dokumen ]", fg=WARNA["teks_sekunder"])
        self.lbl_status.set("Reset! Tambahkan dokumen baru.")
        self._isi_queue_awal()


# ══════════════════════════════════════════════════════════════
#  KASUS 2 — HOT POTATO (Circular Queue)
# ══════════════════════════════════════════════════════════════

class PanelHotPotato(tk.Frame):
    """Panel simulasi Hot Potato dengan Circular Queue di canvas."""

    PEMAIN_AWAL = ["Andi", "Budi", "Cici", "Dina", "Edo", "Fani"]
    HITUNGAN    = 4

    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_panel"])
        self._pemain      = deque(self.PEMAIN_AWAL.copy())
        self._holder_idx  = 0
        self._eliminasi   = []
        self._sedang_anim = False
        self._ronde       = 1
        self._buat_ui()

    def _buat_ui(self):
        tk.Label(self, text="🥔  Hot Potato — Circular Queue",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_utama"],
                 font=FONT["sub_judul"]).pack(anchor="w", padx=20, pady=(16, 4))
        tk.Label(self,
                 text="Pemain melempar kentang berputar. Yang memegang saat berhenti → ELIMINATED!",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"]).pack(anchor="w", padx=20, pady=(0, 8))

        # ── Canvas Lingkaran Pemain ──
        self.canvas = tk.Canvas(self, bg=WARNA["bg_panel"], height=280,
                                highlightthickness=0)
        self.canvas.pack(fill="x", padx=20, pady=4)
        self.canvas.bind("<Configure>", lambda e: self._gambar_lingkaran())

        # ── Info Ronde ──
        frame_info = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_info.pack(fill="x", padx=20, pady=4)

        self.lbl_ronde = tk.Label(frame_info, text="Ronde: 1",
                                  bg=WARNA["bg_panel"], fg=WARNA["aktif"],
                                  font=FONT["sub_judul"])
        self.lbl_ronde.pack(side="left")

        self.lbl_sisa = tk.Label(frame_info, text=f"  Sisa: {len(self._pemain)} pemain",
                                 bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                                 font=FONT["normal"])
        self.lbl_sisa.pack(side="left", padx=16)

        self.lbl_elim = tk.Label(frame_info, text="Eliminated: –",
                                 bg=WARNA["bg_panel"], fg=WARNA["dequeue"],
                                 font=FONT["normal"])
        self.lbl_elim.pack(side="left")

        # ── Log ──
        self.lbl_status = LabelStatus(self, text="  Tekan 'Lempar Kentang' untuk memulai.")
        self.lbl_status.pack(fill="x", padx=20, pady=(0, 6))

        # ── Kontrol ──
        frame_ctrl = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_ctrl.pack(pady=6)
        TombolModern(frame_ctrl, "🥔 Lempar Kentang", WARNA["btn_start"],
                     self._lempar, lebar=18).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "🛑 Stop → Eliminasi", WARNA["btn_dequeue"],
                     self._eliminasi_pemain, lebar=18).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "↺ Reset", WARNA["btn_reset"],
                     self._reset, lebar=10).pack(side="left", padx=6)

    def _gambar_lingkaran(self):
        """Gambar semua pemain dalam lingkaran di canvas."""
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 280
        cx, cy = w // 2, h // 2
        radius = min(cx, cy) - 55
        if radius < 40:
            radius = 40

        pemain_list = list(self._pemain)
        n = len(pemain_list)
        if n == 0:
            return

        import math
        for i, nama in enumerate(pemain_list):
            sudut = (2 * math.pi * i / n) - math.pi / 2
            px    = cx + radius * math.cos(sudut)
            py    = cy + radius * math.sin(sudut)

            # Warna node
            if i == self._holder_idx:
                warna_node = WARNA["dequeue"]
                radius_node = 36
            else:
                warna_node = WARNA["normal"]
                radius_node = 30

            # Gambar lingkaran node
            self.canvas.create_oval(
                px - radius_node, py - radius_node,
                px + radius_node, py + radius_node,
                fill=warna_node, outline="#4A5568", width=2
            )
            # Nama pemain
            self.canvas.create_text(px, py - 6, text=nama[:6],
                                     fill="#FFFFFF", font=FONT["box"])
            # Emoji kentang untuk pemegang
            if i == self._holder_idx:
                self.canvas.create_text(px, py + 12, text="🥔",
                                         font=("Segoe UI", 12))

        # Gambar panah circular di tengah
        self.canvas.create_text(cx, cy, text="↻", fill=WARNA["aktif"],
                                 font=("Segoe UI", 24, "bold"))
        self.canvas.create_text(cx, cy + 20, text="Circular", fill=WARNA["teks_sekunder"],
                                 font=FONT["kecil"])

    def _lempar(self):
        if self._sedang_anim or len(self._pemain) <= 1:
            return
        self._sedang_anim = True
        self._lemparan_ke = 0
        self._lanjut_lempar()

    def _lanjut_lempar(self):
        if self._lemparan_ke >= self.HITUNGAN:
            self._sedang_anim = False
            pemain_aktif = list(self._pemain)[self._holder_idx]
            self.lbl_status.set(f"🛑 Musik berhenti! [{pemain_aktif}] memegang kentang!", WARNA["aktif"])
            return
        # Rotasi 1 langkah
        self._pemain.append(self._pemain.popleft())
        pemegang = list(self._pemain)[self._holder_idx]
        self._lemparan_ke += 1
        self.lbl_status.set(f"Lemparan {self._lemparan_ke}/{self.HITUNGAN}: [{pemegang}] memegang 🥔", WARNA["normal"])
        self._gambar_lingkaran()
        self.after(DELAY_ANIM // 2, self._lanjut_lempar)

    def _eliminasi_pemain(self):
        if len(self._pemain) <= 1:
            if self._pemain:
                messagebox.showinfo("🏆 Selesai!", f"Pemenang: [{self._pemain[0]}]!")
            return
        yang_pegang = list(self._pemain)[self._holder_idx]
        self._pemain.popleft()
        self._eliminasi.append(yang_pegang)
        # Adjust holder index
        if self._holder_idx >= len(self._pemain):
            self._holder_idx = 0
        self._ronde += 1
        self.lbl_ronde.config(text=f"Ronde: {self._ronde}")
        self.lbl_sisa.config(text=f"  Sisa: {len(self._pemain)} pemain")
        self.lbl_elim.config(text=f"Eliminated: {', '.join(self._eliminasi)}")
        self.lbl_status.set(f"💀 [{yang_pegang}] dieliminasi!", WARNA["dequeue"])
        self._gambar_lingkaran()

        if len(self._pemain) == 1:
            self.after(400, lambda: messagebox.showinfo(
                "🏆 Pemenang!", f"[{self._pemain[0]}] adalah pemenang Hot Potato!"))

    def _reset(self):
        self._pemain      = deque(self.PEMAIN_AWAL.copy())
        self._holder_idx  = 0
        self._eliminasi   = []
        self._sedang_anim = False
        self._ronde       = 1
        self.lbl_ronde.config(text="Ronde: 1")
        self.lbl_sisa.config(text=f"  Sisa: {len(self._pemain)} pemain")
        self.lbl_elim.config(text="Eliminated: –")
        self.lbl_status.set("  Reset! Tekan 'Lempar Kentang' untuk mulai.")
        self._gambar_lingkaran()


# ══════════════════════════════════════════════════════════════
#  KASUS 3 — ANTRIAN RUMAH SAKIT (Priority Queue)
# ══════════════════════════════════════════════════════════════

class PanelRumahSakit(tk.Frame):
    """Panel simulasi priority queue rumah sakit."""

    LABEL_PRIO = {1: ("🚨 Darurat", WARNA["prio1"]),
                  2: ("⚠️  Segera",  WARNA["prio2"]),
                  3: ("✅ Normal",   WARNA["prio3"])}
    PASIEN_CONTOH = [
        ("Pak Budi",   "Cek Rutin",        3),
        ("Ibu Cici",   "Demam Tinggi",     2),
        ("Anak Dani",  "Serangan Jantung", 1),
        ("Mbak Eka",   "Patah Tangan",     2),
        ("Pak Faris",  "Kontrol Obat",     3),
        ("Ibu Gina",   "Sesak Napas",      1),
    ]

    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_panel"])
        self._heap    = []    # min-heap
        self._counter = 0     # tiebreaker FIFO
        self._buat_ui()
        self._isi_awal()

    def _buat_ui(self):
        tk.Label(self, text="🏥  Antrian Rumah Sakit — Priority Queue",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_utama"],
                 font=FONT["sub_judul"]).pack(anchor="w", padx=20, pady=(16, 4))
        tk.Label(self,
                 text="Pasien dengan prioritas tertinggi (Darurat) dilayani lebih dulu.",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"]).pack(anchor="w", padx=20, pady=(0, 10))

        # ── Tabel Antrian ──
        frame_tabel = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_tabel.pack(fill="both", expand=True, padx=20, pady=4)

        # Header tabel
        header_data = [("No.", 4), ("Nama Pasien", 16), ("Kondisi", 22), ("Prioritas", 14)]
        for teks, lebar in header_data:
            tk.Label(frame_tabel, text=teks, bg=WARNA["bg_card"],
                     fg=WARNA["teks_label"], font=FONT["normal"],
                     width=lebar, pady=6, relief="flat",
                     anchor="center").pack(side="left", padx=1)

        # Scrollable list menggunakan frame + canvas
        self.frame_antrian = tk.Frame(self, bg=WARNA["bg_panel"])
        self.frame_antrian.pack(fill="x", padx=20)

        # Dokter status
        self.lbl_dokter = tk.Label(self,
                                    text="👨‍⚕️  Dokter: Menunggu pasien...",
                                    bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                                    font=FONT["normal"], anchor="w", pady=8, padx=12)
        self.lbl_dokter.pack(fill="x", padx=20)

        self.lbl_status = LabelStatus(self, text="  Tambah pasien lalu tekan Panggil Pasien.")
        self.lbl_status.pack(fill="x", padx=20)

        # ── Kontrol ──
        frame_ctrl = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_ctrl.pack(pady=8, padx=20)

        # Tambah pasien manual
        tk.Label(frame_ctrl, text="Nama:", bg=WARNA["bg_panel"],
                 fg=WARNA["teks_label"], font=FONT["normal"]).pack(side="left")
        self.entry_nama = tk.Entry(frame_ctrl, width=12, font=FONT["normal"],
                                   bg=WARNA["bg_card"], fg=WARNA["teks_utama"],
                                   insertbackground="white", relief="flat", bd=6)
        self.entry_nama.insert(0, "Pasien X")
        self.entry_nama.pack(side="left", padx=6, ipady=4)

        self.var_prio = tk.IntVar(value=2)
        for val, (label, warna) in self.LABEL_PRIO.items():
            tk.Radiobutton(frame_ctrl, text=label, variable=self.var_prio, value=val,
                           bg=WARNA["bg_panel"], fg=warna, selectcolor=WARNA["bg_card"],
                           font=FONT["kecil"], activebackground=WARNA["bg_panel"]).pack(side="left", padx=4)

        TombolModern(frame_ctrl, "➕ Enqueue", WARNA["btn_enqueue"],
                     self._enqueue, lebar=12).pack(side="left", padx=8)
        TombolModern(frame_ctrl, "👨‍⚕️ Panggil", WARNA["btn_start"],
                     self._dequeue, lebar=12).pack(side="left", padx=4)
        TombolModern(frame_ctrl, "↺ Reset", WARNA["btn_reset"],
                     self._reset, lebar=8).pack(side="left", padx=4)

    def _isi_awal(self):
        for nama, kondisi, prio in self.PASIEN_CONTOH[:4]:
            heapq.heappush(self._heap, (prio, self._counter, nama, kondisi))
            self._counter += 1
        self._refresh_tabel()

    def _refresh_tabel(self):
        """Gambar ulang tabel antrian dari heap yang diurutkan."""
        for w in self.frame_antrian.winfo_children():
            w.destroy()

        if not self._heap:
            tk.Label(self.frame_antrian, text="[ Antrian Kosong ]",
                     bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                     font=FONT["normal"], pady=12).pack()
            return

        disort = sorted(self._heap)
        for idx, (prio, _, nama, kondisi) in enumerate(disort, 1):
            label_prio, warna_prio = self.LABEL_PRIO[prio]
            frame_baris = tk.Frame(self.frame_antrian, bg=WARNA["bg_card" if idx % 2 == 0 else "bg_panel"])
            frame_baris.pack(fill="x", pady=1)

            # Indikator NEXT
            tanda = "← NEXT" if idx == 1 else ""
            tk.Label(frame_baris, text=str(idx), width=4,
                     bg=frame_baris["bg"], fg=WARNA["teks_sekunder"], font=FONT["normal"],
                     pady=5).pack(side="left")
            tk.Label(frame_baris, text=nama, width=16,
                     bg=frame_baris["bg"], fg=WARNA["teks_utama"], font=FONT["normal"]).pack(side="left")
            tk.Label(frame_baris, text=kondisi, width=22,
                     bg=frame_baris["bg"], fg=WARNA["teks_sekunder"], font=FONT["normal"]).pack(side="left")
            tk.Label(frame_baris, text=label_prio, width=14,
                     bg=frame_baris["bg"], fg=warna_prio, font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(frame_baris, text=tanda, bg=frame_baris["bg"],
                     fg=WARNA["aktif"], font=FONT["kecil"]).pack(side="left")

    def _enqueue(self):
        nama = self.entry_nama.get().strip()
        if not nama:
            messagebox.showwarning("Input Kosong", "Masukkan nama pasien!")
            return
        prio = self.var_prio.get()
        kondisi = {"1":"Darurat","2":"Perlu perhatian","3":"Cek rutin"}[str(prio)]
        heapq.heappush(self._heap, (prio, self._counter, nama, kondisi))
        self._counter += 1
        label_prio, _ = self.LABEL_PRIO[prio]
        self.lbl_status.set(f"ENQUEUE: {nama} ({label_prio}) masuk antrian!", WARNA["enqueue"])
        self._refresh_tabel()

    def _dequeue(self):
        if not self._heap:
            self.lbl_status.set("Antrian kosong!", WARNA["dequeue"])
            return
        prio, _, nama, kondisi = heapq.heappop(self._heap)
        label_prio, warna_prio = self.LABEL_PRIO[prio]
        self.lbl_dokter.config(
            text=f"👨‍⚕️  Dokter sedang menangani: {nama}  ({label_prio} — {kondisi})",
            fg=warna_prio
        )
        self.lbl_status.set(f"DEQUEUE: {nama} ({label_prio}) dipanggil ke dokter!", warna_prio)
        self._refresh_tabel()

    def _reset(self):
        self._heap    = []
        self._counter = 0
        self.lbl_dokter.config(text="👨‍⚕️  Dokter: Menunggu pasien...", fg=WARNA["teks_sekunder"])
        self.lbl_status.set("  Reset! Antrian dikosongkan.")
        self._refresh_tabel()
        self._isi_awal()


# ══════════════════════════════════════════════════════════════
#  KASUS 4 — BFS (Breadth First Search)
# ══════════════════════════════════════════════════════════════

class PanelBFS(tk.Frame):
    """Panel BFS traversal — graph digambar di canvas, node berubah warna."""

    # Posisi relatif node dalam graph
    NODE_POS = {
        "A": (0.50, 0.12),
        "B": (0.28, 0.38),
        "C": (0.72, 0.38),
        "D": (0.14, 0.68),
        "E": (0.40, 0.68),
        "F": (0.60, 0.68),
        "G": (0.86, 0.68),
        "H": (0.50, 0.92),
    }
    EDGES = [
        ("A","B"),("A","C"),
        ("B","D"),("B","E"),
        ("C","F"),("C","G"),
        ("E","H"),("F","H"),
    ]
    GRAPH = {
        "A": ["B","C"],
        "B": ["A","D","E"],
        "C": ["A","F","G"],
        "D": ["B"],
        "E": ["B","H"],
        "F": ["C","H"],
        "G": ["C"],
        "H": ["E","F"],
    }

    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_panel"])
        self._reset_state()
        self._buat_ui()

    def _reset_state(self):
        self._bfs_queue   = deque()
        self._dikunjungi  = set()
        self._urutan      = []
        self._warna_node  = {n: "unvisited" for n in self.NODE_POS}
        self._langkah     = 0
        self._selesai     = False

    def _buat_ui(self):
        tk.Label(self, text="🔍  BFS Traversal — Queue untuk Graph",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_utama"],
                 font=FONT["sub_judul"]).pack(anchor="w", padx=20, pady=(16,4))
        tk.Label(self,
                 text="BFS menjelajahi graph per level menggunakan Queue FIFO.",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"]).pack(anchor="w", padx=20, pady=(0,8))

        # ── Layout: canvas graph + panel info ──
        frame_main = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_main.pack(fill="both", expand=True, padx=20, pady=4)

        # Canvas graph
        self.canvas = tk.Canvas(frame_main, bg=WARNA["bg_panel"],
                                width=420, height=280, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._gambar_graph())

        # Panel kanan — info
        frame_info = tk.Frame(frame_main, bg=WARNA["bg_panel"], width=240)
        frame_info.pack(side="right", fill="y", padx=(12,0))
        frame_info.pack_propagate(False)

        tk.Label(frame_info, text="BFS Queue:", bg=WARNA["bg_panel"],
                 fg=WARNA["teks_label"], font=FONT["normal"]).pack(anchor="w", pady=(4,2))
        self.lbl_bfs_q = tk.Label(frame_info, text="[ ]",
                                   bg=WARNA["bg_card"], fg=WARNA["aktif"],
                                   font=FONT["mono"], pady=6, padx=8, anchor="w",
                                   wraplength=220, justify="left")
        self.lbl_bfs_q.pack(fill="x", pady=(0,8))

        tk.Label(frame_info, text="Sudah dikunjungi:", bg=WARNA["bg_panel"],
                 fg=WARNA["teks_label"], font=FONT["normal"]).pack(anchor="w", pady=(4,2))
        self.lbl_visited = tk.Label(frame_info, text="–",
                                     bg=WARNA["bg_card"], fg=WARNA["enqueue"],
                                     font=FONT["mono"], pady=6, padx=8, anchor="w",
                                     wraplength=220, justify="left")
        self.lbl_visited.pack(fill="x", pady=(0,8))

        # Legenda warna
        tk.Label(frame_info, text="Keterangan Warna:", bg=WARNA["bg_panel"],
                 fg=WARNA["teks_label"], font=FONT["kecil"]).pack(anchor="w", pady=(8,4))
        legenda = [
            (WARNA["bg_card"],   "Belum dikunjungi"),
            (WARNA["aktif"],     "Saat ini diproses"),
            (WARNA["highlight"], "Dalam queue"),
            (WARNA["enqueue"],   "Sudah dikunjungi"),
        ]
        for warna, label in legenda:
            f = tk.Frame(frame_info, bg=WARNA["bg_panel"])
            f.pack(anchor="w")
            tk.Label(f, text="●", bg=WARNA["bg_panel"], fg=warna,
                     font=("Segoe UI", 14)).pack(side="left")
            tk.Label(f, text=label, bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                     font=FONT["kecil"]).pack(side="left")

        # ── Log & Kontrol ──
        self.lbl_status = LabelStatus(self, text="  Tekan 'Mulai BFS' atau '▶ Langkah' untuk traversal.")
        self.lbl_status.pack(fill="x", padx=20)

        frame_ctrl = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_ctrl.pack(pady=8)
        TombolModern(frame_ctrl, "▶ Langkah", WARNA["btn_start"],
                     self._langkah_bfs, lebar=12).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "⏩ Auto BFS", WARNA["btn_enqueue"],
                     self._auto_bfs, lebar=12).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "↺ Reset", WARNA["btn_reset"],
                     self._reset, lebar=10).pack(side="left", padx=6)

    def _warna_untuk(self, node):
        status = self._warna_node.get(node, "unvisited")
        return {
            "unvisited" : WARNA["bg_card"],
            "queued"    : WARNA["highlight"],
            "current"   : WARNA["aktif"],
            "visited"   : WARNA["enqueue"],
        }.get(status, WARNA["bg_card"])

    def _gambar_graph(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 420
        h = self.canvas.winfo_height() or 280

        # Gambar edges
        for a, b in self.EDGES:
            ax, ay = self.NODE_POS[a][0]*w, self.NODE_POS[a][1]*h
            bx, by = self.NODE_POS[b][0]*w, self.NODE_POS[b][1]*h
            self.canvas.create_line(ax, ay, bx, by, fill="#334155", width=2)

        # Gambar node
        R = 22
        for node, (rx, ry) in self.NODE_POS.items():
            px, py = rx * w, ry * h
            warna  = self._warna_untuk(node)
            self.canvas.create_oval(px-R, py-R, px+R, py+R,
                                     fill=warna, outline="#4A5568", width=2)
            self.canvas.create_text(px, py, text=node, fill="#FFFFFF",
                                     font=("Segoe UI", 12, "bold"))

    def _langkah_bfs(self):
        if self._selesai:
            return

        # Inisialisasi
        if self._langkah == 0:
            self._bfs_queue.append("A")
            self._dikunjungi.add("A")
            self._warna_node["A"] = "queued"
            self.lbl_status.set("ENQUEUE 'A' ke queue — BFS dimulai!", WARNA["highlight"])
            self._gambar_graph()
            self._update_info()
            self._langkah += 1
            return

        if not self._bfs_queue:
            self._selesai = True
            self.lbl_status.set(f"✅ BFS Selesai! Urutan: {' → '.join(self._urutan)}", WARNA["enqueue"])
            return

        # Dequeue node aktif
        node = self._bfs_queue.popleft()
        self._urutan.append(node)

        # Reset warna node sebelumnya ke visited
        for n in self._warna_node:
            if self._warna_node[n] == "current":
                self._warna_node[n] = "visited"
        self._warna_node[node] = "current"

        # Enqueue tetangga baru
        tetangga_baru = []
        for tetangga in self.GRAPH.get(node, []):
            if tetangga not in self._dikunjungi:
                self._dikunjungi.add(tetangga)
                self._bfs_queue.append(tetangga)
                self._warna_node[tetangga] = "queued"
                tetangga_baru.append(tetangga)

        pesan = f"Kunjungi '{node}'"
        if tetangga_baru:
            pesan += f" → Enqueue: {tetangga_baru}"
        self.lbl_status.set(pesan, WARNA["aktif"])
        self._gambar_graph()
        self._update_info()
        self._langkah += 1

    def _update_info(self):
        q_str = str(list(self._bfs_queue)) if self._bfs_queue else "[ Kosong ]"
        self.lbl_bfs_q.config(text=q_str)
        v_str = " → ".join(self._urutan) if self._urutan else "–"
        self.lbl_visited.config(text=v_str)

    def _auto_bfs(self):
        if self._selesai:
            return
        self._langkah_bfs()
        if not self._selesai:
            self.after(DELAY_ANIM, self._auto_bfs)

    def _reset(self):
        self._reset_state()
        self.lbl_bfs_q.config(text="[ ]")
        self.lbl_visited.config(text="–")
        self.lbl_status.set("  Reset! Tekan 'Langkah' atau 'Auto BFS'.")
        self._gambar_graph()


# ══════════════════════════════════════════════════════════════
#  KASUS 5 — LOKET BANDARA (Multi-Server Queue)
# ══════════════════════════════════════════════════════════════

class PanelBandara(tk.Frame):
    """Panel simulasi multi-server queue di bandara."""

    PENUMPANG_CONTOH = [
        ("Andi", "Jakarta"), ("Bela", "Surabaya"), ("Coco", "Bali"),
        ("Dita", "Medan"),   ("Evan", "Makassar"),  ("Fika", "Yogya"),
        ("Gani", "Lombok"),  ("Hana", "Manado"),
    ]

    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_panel"])
        self._antrian      = deque()
        self._loket        = {"Loket 1": None, "Loket 2": None}
        self._counter_pnp  = 0
        self._total_done   = 0
        self._buat_ui()
        self._isi_awal()

    def _buat_ui(self):
        tk.Label(self, text="✈️  Loket Bandara — Multi-Server Queue",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_utama"],
                 font=FONT["sub_judul"]).pack(anchor="w", padx=20, pady=(16,4))
        tk.Label(self,
                 text="Satu antrian umum → penumpang diarahkan ke loket kosong (FIFO).",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"]).pack(anchor="w", padx=20, pady=(0,10))

        # ── Layout utama ──
        frame_main = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_main.pack(fill="both", expand=True, padx=20, pady=4)

        # Kolom antrian
        frame_antri = tk.Frame(frame_main, bg=WARNA["bg_panel"])
        frame_antri.pack(side="left", fill="both", expand=True)

        tk.Label(frame_antri, text="📋 Antrian Penumpang (FRONT → REAR):",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_label"],
                 font=FONT["normal"]).pack(anchor="w")

        self.canvas_antrian = BoxQueue(frame_antri, tinggi=110)
        self.canvas_antrian.pack(fill="x", pady=4)

        # Kolom loket
        frame_loket = tk.Frame(frame_main, bg=WARNA["bg_panel"], width=240)
        frame_loket.pack(side="right", fill="y", padx=(16,0))
        frame_loket.pack_propagate(False)

        tk.Label(frame_loket, text="🪧 Status Loket:",
                 bg=WARNA["bg_panel"], fg=WARNA["teks_label"],
                 font=FONT["normal"]).pack(anchor="w", pady=(0,6))

        self.frame_loket_boxes = tk.Frame(frame_loket, bg=WARNA["bg_panel"])
        self.frame_loket_boxes.pack(fill="x")

        # ── Statistik ──
        self.lbl_total = tk.Label(self, text="Total dilayani: 0",
                                   bg=WARNA["bg_panel"], fg=WARNA["teks_sekunder"],
                                   font=FONT["normal"], anchor="w", padx=20)
        self.lbl_total.pack(fill="x")

        # ── Log ──
        self.lbl_status = LabelStatus(self, text="  Tambah penumpang lalu layani ke loket.")
        self.lbl_status.pack(fill="x", padx=20)

        # ── Kontrol ──
        frame_ctrl = tk.Frame(self, bg=WARNA["bg_panel"])
        frame_ctrl.pack(pady=8)

        TombolModern(frame_ctrl, "🧍 + Penumpang", WARNA["btn_enqueue"],
                     self._enqueue, lebar=16).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "✈️ Layani (Dequeue)", WARNA["btn_start"],
                     self._dequeue, lebar=18).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "⏩ Auto Simulasi", WARNA["btn_dequeue"],
                     self._auto_simulasi, lebar=16).pack(side="left", padx=6)
        TombolModern(frame_ctrl, "↺ Reset", WARNA["btn_reset"],
                     self._reset, lebar=10).pack(side="left", padx=6)

    def _isi_awal(self):
        for nama, tujuan in self.PENUMPANG_CONTOH[:5]:
            self._antrian.append((nama, tujuan))
        self._refresh_all()

    def _refresh_all(self):
        # Perbarui canvas antrian
        items = [f"{p[0]}\n→{p[1]}" for p in self._antrian]
        self.canvas_antrian.gambar_queue(items)
        # Perbarui tampilan loket
        self._refresh_loket()

    def _refresh_loket(self):
        for w in self.frame_loket_boxes.winfo_children():
            w.destroy()

        for nama_loket, isi in self._loket.items():
            sibuk   = isi is not None
            warna   = WARNA["loket_sibuk"] if sibuk else WARNA["loket_kosong"]
            status  = f"🔴 {isi[0]} → {isi[1]}" if sibuk else "🟢 Kosong — Siap"
            f = tk.Frame(self.frame_loket_boxes,
                         bg=WARNA["bg_card"], pady=10, padx=12)
            f.pack(fill="x", pady=4)
            tk.Label(f, text=f"🪧 {nama_loket}", bg=WARNA["bg_card"],
                     fg=warna, font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(f, text=status, bg=WARNA["bg_card"],
                     fg=WARNA["teks_label"], font=FONT["kecil"]).pack(anchor="w")
            if sibuk:
                TombolModern(f, "✅ Selesai", WARNA["btn_reset"],
                             lambda l=nama_loket: self._selesai_loket(l),
                             lebar=12).pack(anchor="w", pady=(6,0))

    def _enqueue(self):
        if self._counter_pnp >= len(self.PENUMPANG_CONTOH):
            self._counter_pnp = 0
        nama, tujuan = self.PENUMPANG_CONTOH[self._counter_pnp]
        self._counter_pnp += 1
        self._antrian.append((nama, tujuan))
        self.lbl_status.set(f"ENQUEUE: {nama} (→{tujuan}) bergabung antrian!", WARNA["enqueue"])
        self._refresh_all()

    def _dequeue(self):
        loket_kosong = next((l for l, v in self._loket.items() if v is None), None)
        if not loket_kosong:
            self.lbl_status.set("Semua loket sedang sibuk!", WARNA["aktif"])
            return
        if not self._antrian:
            self.lbl_status.set("Antrian kosong!", WARNA["dequeue"])
            return
        pnp = self._antrian.popleft()
        self._loket[loket_kosong] = pnp
        self.lbl_status.set(
            f"DEQUEUE: {pnp[0]} diarahkan ke {loket_kosong}!", WARNA["normal"])
        self._refresh_all()

    def _selesai_loket(self, nama_loket):
        pnp = self._loket[nama_loket]
        if pnp:
            self._loket[nama_loket] = None
            self._total_done += 1
            self.lbl_total.config(text=f"Total dilayani: {self._total_done} penumpang")
            self.lbl_status.set(f"✅ {pnp[0]} selesai check-in di {nama_loket}!", WARNA["enqueue"])
            self._refresh_all()

    def _auto_simulasi(self):
        self._dequeue()
        if self._antrian or any(v for v in self._loket.values()):
            self.after(DELAY_ANIM, self._auto_simulasi)

    def _reset(self):
        self._antrian     = deque()
        self._loket       = {"Loket 1": None, "Loket 2": None}
        self._counter_pnp = 0
        self._total_done  = 0
        self.lbl_total.config(text="Total dilayani: 0")
        self.lbl_status.set("  Reset! Antrian dikosongkan.")
        self._refresh_all()
        self._isi_awal()


# ══════════════════════════════════════════════════════════════
#  APLIKASI UTAMA
# ══════════════════════════════════════════════════════════════

class AplikasiQueue(tk.Tk):
    """
    Window utama aplikasi.
    Layout: Header → Sidebar (kiri) + Area Utama (kanan)
    """

    MENU_SIMULASI = [
        ("🖨️  Antrian Printer",    PanelPrinter),
        ("🥔  Hot Potato",          PanelHotPotato),
        ("🏥  Antrian Rumah Sakit", PanelRumahSakit),
        ("🔍  BFS Traversal",       PanelBFS),
        ("✈️  Loket Bandara",       PanelBandara),
    ]

    def __init__(self):
        super().__init__()
        self.title("Simulasi Queue — Struktur Data | D4 Manajemen Informatika")
        self.geometry(f"{LEBAR_APP}x{TINGGI_APP}")
        self.minsize(900, 600)
        self.configure(bg=WARNA["bg_utama"])
        self.resizable(True, True)

        # Simpan panel yang sudah dibuat (lazy loading)
        self._panel_cache = {}
        self._panel_aktif = None

        self._buat_header()
        self._buat_layout()
        self._buat_sidebar()
        self._buat_area_utama()

        # Tampilkan panel pertama
        self._pilih_simulasi(0)

    def _buat_header(self):
        """Header bar di bagian atas."""
        frame_header = tk.Frame(self, bg=WARNA["bg_header"], pady=14)
        frame_header.pack(fill="x")

        tk.Label(
            frame_header,
            text="  🗂️  SIMULASI QUEUE",
            bg=WARNA["bg_header"],
            fg=WARNA["teks_utama"],
            font=FONT["judul"]
        ).pack(side="left")

        tk.Label(
            frame_header,
            text="D4 Manajemen Informatika  |  Struktur Data  |  Semester 2",
            bg=WARNA["bg_header"],
            fg=WARNA["teks_sekunder"],
            font=FONT["kecil"]
        ).pack(side="left", padx=20)

        # Tombol keluar
        TombolModern(
            frame_header, "✕ Keluar", "#7F1D1D",
            self.destroy, lebar=8
        ).pack(side="right", padx=16)

        # Separator
        tk.Frame(self, bg="#334155", height=1).pack(fill="x")

    def _buat_layout(self):
        """Frame utama yang terdiri dari sidebar + area konten."""
        self.frame_layout = tk.Frame(self, bg=WARNA["bg_utama"])
        self.frame_layout.pack(fill="both", expand=True)

    def _buat_sidebar(self):
        """Sidebar kiri berisi menu pilihan simulasi."""
        self.frame_sidebar = tk.Frame(
            self.frame_layout, bg=WARNA["bg_sidebar"],
            width=210, padx=0
        )
        self.frame_sidebar.pack(side="left", fill="y")
        self.frame_sidebar.pack_propagate(False)

        # Separator vertikal
        tk.Frame(self.frame_layout, bg="#334155", width=1).pack(side="left", fill="y")

        tk.Label(self.frame_sidebar, text="  Pilih Simulasi",
                 bg=WARNA["bg_sidebar"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"], pady=14).pack(anchor="w")

        self._tombol_sidebar = []
        for i, (label, _) in enumerate(self.MENU_SIMULASI):
            btn = tk.Button(
                self.frame_sidebar,
                text=f"  {label}",
                command=lambda idx=i: self._pilih_simulasi(idx),
                bg=WARNA["bg_sidebar"],
                fg=WARNA["teks_label"],
                font=FONT["sidebar"],
                relief="flat",
                anchor="w",
                padx=12,
                pady=10,
                cursor="hand2",
                width=26,
                activebackground=WARNA["bg_card"],
                activeforeground=WARNA["teks_utama"],
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=WARNA["bg_card"]) if b["bg"] != WARNA["normal"] else None)
            btn.bind("<Leave>", lambda e, b=btn, idx=i: b.config(bg=WARNA["bg_sidebar"]) if self._idx_aktif != idx else None)
            self._tombol_sidebar.append(btn)

        self._idx_aktif = -1

        # Info di bawah sidebar
        tk.Frame(self.frame_sidebar, bg="#334155", height=1).pack(fill="x", pady=8)
        tk.Label(self.frame_sidebar,
                 text="  Queue = FIFO\n  (First In, First Out)",
                 bg=WARNA["bg_sidebar"], fg=WARNA["teks_sekunder"],
                 font=FONT["kecil"], justify="left").pack(anchor="w", padx=8)

    def _buat_area_utama(self):
        """Area konten di sebelah kanan sidebar."""
        self.frame_konten = tk.Frame(self.frame_layout, bg=WARNA["bg_panel"])
        self.frame_konten.pack(side="right", fill="both", expand=True)

    def _pilih_simulasi(self, idx):
        """Tampilkan panel simulasi sesuai pilihan."""
        if idx == self._idx_aktif:
            return

        # Reset warna tombol sidebar
        for i, btn in enumerate(self._tombol_sidebar):
            if i == idx:
                btn.config(bg=WARNA["normal"], fg="#FFFFFF")
            else:
                btn.config(bg=WARNA["bg_sidebar"], fg=WARNA["teks_label"])
        self._idx_aktif = idx

        # Sembunyikan panel aktif
        if self._panel_aktif:
            self._panel_aktif.pack_forget()

        # Lazy-load panel
        if idx not in self._panel_cache:
            _, KelasPanel = self.MENU_SIMULASI[idx]
            panel = KelasPanel(self.frame_konten)
            self._panel_cache[idx] = panel

        self._panel_aktif = self._panel_cache[idx]
        self._panel_aktif.pack(fill="both", expand=True)


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = AplikasiQueue()
    app.mainloop()