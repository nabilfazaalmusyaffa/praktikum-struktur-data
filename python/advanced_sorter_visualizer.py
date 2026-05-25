"""
====================================================
  Advanced Sorter & ExprHeapSorter — Visualizer
  Tugas Analisis & Desain Algoritma — Bab 12 & 13
====================================================
Jalankan:  python advanced_sorter_visualizer.py
Requires:  matplotlib, tkinter (sudah bawaan Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrowPatch
import time, math, random
from collections import deque
from typing import List, Optional


# ─────────────────────────────────────────────
#  WARNA TEMA
# ─────────────────────────────────────────────
BG        = "#0F1117"
PANEL     = "#1A1D27"
CARD      = "#22263A"
ACCENT    = "#1D9E75"
ACCENT2   = "#378ADD"
ACCENT3   = "#D85A30"
ACCENT4   = "#EF9F27"
PURPLE    = "#7F77DD"
TEXT      = "#E8E8F0"
TEXT_DIM  = "#6B7280"
BORDER    = "#2D3148"

PLT_BG    = "#1A1D27"
PLT_AX    = "#22263A"


# ─────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────
class ListNode:
    def __init__(self, data, nxt=None):
        self.data = data
        self.next = nxt


# ─────────────────────────────────────────────
#  ALGORITMA — Merge Sort Array
# ─────────────────────────────────────────────
class MergeSorter:
    def __init__(self, arr: List[int]):
        self.arr = arr[:]
        self.tmp = [0] * len(arr)
        self.steps = []          # snapshots: (arr_copy, hi_indices, label)
        self.comparisons = 0
        self.copies = 0
        self.max_depth = 0

    def sort(self):
        self._rec(0, len(self.arr) - 1, 0)

    def _rec(self, first, last, depth):
        if first >= last:
            return
        self.max_depth = max(self.max_depth, depth)
        mid = (first + last) // 2
        self._rec(first, mid, depth + 1)
        self._rec(mid + 1, last, depth + 1)
        self._merge(first, mid, last)

    def _merge(self, ls, mid, re):
        a, b, k = ls, mid + 1, ls
        while a <= mid and b <= re:
            self.comparisons += 1
            if self.arr[a] <= self.arr[b]:
                self.tmp[k] = self.arr[a]; a += 1
            else:
                self.tmp[k] = self.arr[b]; b += 1
            k += 1
        while a <= mid:
            self.tmp[k] = self.arr[a]; a += 1; k += 1
        while b <= re:
            self.tmp[k] = self.arr[b]; b += 1; k += 1
        for i in range(ls, re + 1):
            self.arr[i] = self.tmp[i]; self.copies += 1
        hi = list(range(ls, re + 1))
        label = f"Merge [{ls}..{re}] → {self.arr[ls:re+1]}"
        self.steps.append((self.arr[:], hi, label))


# ─────────────────────────────────────────────
#  ALGORITMA — Linked List Merge Sort
# ─────────────────────────────────────────────
class LinkedListSorter:
    def __init__(self, values: List[int]):
        self.original = values[:]
        self.steps = []

    def _make_list(self, vals):
        head = None
        for v in reversed(vals):
            head = ListNode(v, head)
        return head

    def _to_list(self, head):
        result = []
        cur = head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def _split(self, head):
        mid, cur = head, head.next
        while cur and cur.next:
            mid = mid.next
            cur = cur.next.next
        right = mid.next
        mid.next = None
        return right

    def _merge(self, a, b):
        dummy = ListNode(0)
        tail = dummy
        while a and b:
            if a.data <= b.data:
                tail.next = a; a = a.next
            else:
                tail.next = b; b = b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next

    def _sort(self, head):
        if not head or not head.next:
            return head
        right = self._split(head)
        self.steps.append(("split", self._to_list(head), self._to_list(right)))
        left_sorted  = self._sort(head)
        right_sorted = self._sort(right)
        merged = self._merge(left_sorted, right_sorted)
        self.steps.append(("merge", self._to_list(merged), []))
        return merged

    def sort(self):
        head = self._make_list(self.original)
        return self._sort(head)


# ─────────────────────────────────────────────
#  ALGORITMA — Quick Sort
# ─────────────────────────────────────────────
class QuickSorter:
    def __init__(self, arr: List[int]):
        self.arr = arr[:]
        self.steps = []
        self.comparisons = 0
        self.max_depth = 0

    def sort(self):
        self._qs(0, len(self.arr) - 1, 0)

    def _median_pivot(self, lo, hi):
        mid = (lo + hi) // 2
        a, b, c = self.arr[lo], self.arr[mid], self.arr[hi]
        if (a <= b <= c) or (c <= b <= a): return mid
        if (b <= a <= c) or (c <= a <= b): return lo
        return hi

    def _qs(self, lo, hi, depth):
        if lo >= hi: return
        self.max_depth = max(self.max_depth, depth)
        pi = self._median_pivot(lo, hi)
        self.arr[lo], self.arr[pi] = self.arr[pi], self.arr[lo]
        pivot = self.arr[lo]
        i, j = lo + 1, hi
        while i <= j:
            self.comparisons += 1
            while i <= j and self.arr[i] <= pivot: i += 1; self.comparisons += 1
            while i <= j and self.arr[j] > pivot:  j -= 1; self.comparisons += 1
            if i < j:
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        self.arr[lo], self.arr[j] = self.arr[j], self.arr[lo]
        self.steps.append((self.arr[:], j, lo, hi,
                           f"depth={depth} pivot={pivot} pos={j}"))
        self._qs(lo, j - 1, depth + 1)
        self._qs(j + 1, hi, depth + 1)


# ─────────────────────────────────────────────
#  ALGORITMA — Expression Tree
# ─────────────────────────────────────────────
class ExprNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.x = self.y = 0.0

class ExprTree:
    def __init__(self, expr: str):
        self.expr = expr.replace(" ", "")
        self.root = None
        self.postfix = []
        self.result = None

    def build(self):
        tokens = deque(self.expr)
        state = {"i": 0}
        chars = list(self.expr)

        def parse(pos):
            if pos >= len(chars): return None, pos
            ch = chars[pos]
            if ch == "(":
                pos += 1
                left, pos  = parse(pos)
                op  = chars[pos]; pos += 1
                right, pos = parse(pos)
                if pos < len(chars) and chars[pos] == ")": pos += 1
                return ExprNode(op, left, right), pos
            else:
                num = ""
                while pos < len(chars) and (chars[pos].isdigit() or chars[pos] == "."):
                    num += chars[pos]; pos += 1
                return ExprNode(num), pos

        self.root, _ = parse(0)
        self._layout(self.root, 0, 0, 1)
        self._normalize(self.root)
        self.postfix = []
        self._postorder(self.root, self.postfix)
        self.result = self._eval(self.root)

    def _eval(self, node):
        if not node: return 0
        if not node.left and not node.right: return float(node.val)
        l, r = self._eval(node.left), self._eval(node.right)
        if node.val == "+": return l + r
        if node.val == "-": return l - r
        if node.val == "*": return l * r
        if node.val == "/":
            if r == 0: raise ValueError("Division by zero")
            return l / r

    def _postorder(self, node, out):
        if not node: return
        self._postorder(node.left, out)
        self._postorder(node.right, out)
        out.append(node.val)

    def _layout(self, node, depth, left, right):
        if not node: return
        mid = (left + right) / 2
        node.x = mid; node.y = -depth
        self._layout(node.left,  depth+1, left, mid)
        self._layout(node.right, depth+1, mid,  right)

    def _normalize(self, node):
        if not node: return
        self._normalize(node.left)
        self._normalize(node.right)


# ─────────────────────────────────────────────
#  ALGORITMA — Heap Sort
# ─────────────────────────────────────────────
class HeapSorter:
    def __init__(self, arr: List[int]):
        self.arr = arr[:]
        self.steps = []   # (arr_copy, heap_size, swapped_pair, phase_label)
        self.comparisons = 0
        self.swaps = 0

    def sort(self):
        arr = self.arr[:]
        n = len(arr)
        # Phase 1: build max-heap
        for i in range(n // 2 - 1, -1, -1):
            self._sift(arr, n, i, "Build Heap")
        # Phase 2: extract
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]; self.swaps += 1
            self.steps.append((arr[:], end, (0, end), f"Extract → pos {end}"))
            self._sift(arr, end, 0, "Sift Down")
        self.arr = arr

    def _sift(self, arr, size, idx, phase):
        while True:
            largest = idx
            l, r = 2*idx+1, 2*idx+2
            self.comparisons += 1
            if l < size and arr[l] > arr[largest]: largest = l
            self.comparisons += 1
            if r < size and arr[r] > arr[largest]: largest = r
            if largest == idx: break
            arr[idx], arr[largest] = arr[largest], arr[idx]; self.swaps += 1
            self.steps.append((arr[:], size, (idx, largest), phase))
            idx = largest


# ─────────────────────────────────────────────
#  TKINTER UI
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Sorter & ExprHeapSorter — Visualizer")
        self.configure(bg=BG)
        self.geometry("1100x720")
        self.resizable(True, True)

        self._style()
        self._sidebar()
        self._main_area()
        self._show_panel("merge")

    # ── Style ──
    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background=BG)
        s.configure("Card.TFrame", background=CARD)
        s.configure("TLabel", background=BG, foreground=TEXT,
                    font=("Helvetica", 11))
        s.configure("Dim.TLabel", background=BG, foreground=TEXT_DIM,
                    font=("Helvetica", 10))
        s.configure("Title.TLabel", background=BG, foreground=TEXT,
                    font=("Helvetica", 14, "bold"))
        s.configure("Stat.TLabel", background=CARD, foreground=TEXT,
                    font=("Courier", 13, "bold"))
        s.configure("StatLbl.TLabel", background=CARD, foreground=TEXT_DIM,
                    font=("Helvetica", 9))
        s.configure("TButton",
                    background=CARD, foreground=TEXT,
                    bordercolor=BORDER, focuscolor=ACCENT,
                    font=("Helvetica", 10), padding=(8, 4))
        s.map("TButton",
              background=[("active", ACCENT), ("pressed", ACCENT)],
              foreground=[("active", "#ffffff")])
        s.configure("Accent.TButton",
                    background=ACCENT, foreground="#ffffff",
                    bordercolor=ACCENT, font=("Helvetica", 10, "bold"))
        s.map("Accent.TButton",
              background=[("active", "#0F6E56")])
        s.configure("Nav.TButton",
                    background=PANEL, foreground=TEXT_DIM,
                    bordercolor=PANEL, font=("Helvetica", 10),
                    padding=(10, 8), anchor="w")
        s.map("Nav.TButton",
              background=[("active", CARD)],
              foreground=[("active", TEXT)])
        s.configure("Active.Nav.TButton",
                    background=CARD, foreground=ACCENT,
                    bordercolor=CARD, font=("Helvetica", 10, "bold"),
                    padding=(10, 8), anchor="w")
        s.configure("TScale", background=BG, troughcolor=CARD,
                    slidercolor=ACCENT)

    # ── Sidebar ──
    def _sidebar(self):
        side = tk.Frame(self, bg=PANEL, width=190)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="⚙ Algoritma",
                 bg=PANEL, fg=TEXT_DIM,
                 font=("Helvetica", 9, "bold")).pack(pady=(18,4), padx=14, anchor="w")

        self.nav_btns = {}
        items = [
            ("merge",  "📊  Merge Sort"),
            ("ll",     "🔗  Linked List Sort"),
            ("quick",  "⚡  Quick Sort"),
            ("expr",   "🌳  Expression Tree"),
            ("heap",   "🏔  Heap Sort"),
        ]
        for key, label in items:
            b = tk.Button(side, text=label, bg=PANEL, fg=TEXT_DIM,
                          relief="flat", anchor="w",
                          font=("Helvetica", 10), padx=14, pady=7,
                          activebackground=CARD, activeforeground=ACCENT,
                          command=lambda k=key: self._show_panel(k))
            b.pack(fill="x", padx=4)
            self.nav_btns[key] = b

        tk.Frame(side, bg=BORDER, height=1).pack(fill="x", padx=14, pady=12)
        tk.Label(side, text="Tugas Bab 12 & 13\nAnalisis Algoritma",
                 bg=PANEL, fg=TEXT_DIM,
                 font=("Helvetica", 8), justify="center").pack(pady=4)

    def _highlight_nav(self, key):
        for k, b in self.nav_btns.items():
            if k == key:
                b.configure(bg=CARD, fg=ACCENT, font=("Helvetica",10,"bold"))
            else:
                b.configure(bg=PANEL, fg=TEXT_DIM, font=("Helvetica",10))

    # ── Main Area ──
    def _main_area(self):
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self.panels = {}
        self.panels["merge"] = self._panel_merge(self.main)
        self.panels["ll"]    = self._panel_ll(self.main)
        self.panels["quick"] = self._panel_quick(self.main)
        self.panels["expr"]  = self._panel_expr(self.main)
        self.panels["heap"]  = self._panel_heap(self.main)

    def _show_panel(self, key):
        for p in self.panels.values():
            p.pack_forget()
        self.panels[key].pack(fill="both", expand=True)
        self._highlight_nav(key)

    # ── Helper: stat card ──
    def _stat_card(self, parent, label):
        f = tk.Frame(parent, bg=CARD, bd=0, relief="flat",
                     highlightbackground=BORDER, highlightthickness=1)
        val = tk.Label(f, text="0", bg=CARD, fg=TEXT,
                       font=("Courier", 18, "bold"))
        val.pack(pady=(6,0))
        tk.Label(f, text=label, bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica", 9)).pack(pady=(0,6))
        return f, val

    def _make_fig(self, h=3.2):
        fig, ax = plt.subplots(figsize=(8, h), facecolor=PLT_BG)
        ax.set_facecolor(PLT_AX)
        ax.tick_params(colors=TEXT_DIM)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        return fig, ax

    def _embed_fig(self, fig, parent):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().configure(bg=PLT_BG)
        return canvas

    # ── Log widget ──
    def _log_widget(self, parent):
        f = tk.Frame(parent, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        txt = tk.Text(f, height=5, bg=CARD, fg=ACCENT, insertbackground=TEXT,
                      font=("Courier", 9), relief="flat", padx=8, pady=6,
                      state="disabled")
        sb = tk.Scrollbar(f, command=txt.yview, bg=BORDER)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        txt.pack(fill="both", expand=True)
        return f, txt

    def _log(self, txt_widget, msg, tag="info"):
        colors = {"info": ACCENT2, "ok": ACCENT, "warn": ACCENT3,
                  "pivot": ACCENT4, "dim": TEXT_DIM}
        txt_widget.configure(state="normal")
        txt_widget.tag_configure(tag, foreground=colors.get(tag, TEXT))
        txt_widget.insert("end", msg + "\n", tag)
        txt_widget.see("end")
        txt_widget.configure(state="disabled")

    def _clear_log(self, txt_widget):
        txt_widget.configure(state="normal")
        txt_widget.delete("1.0", "end")
        txt_widget.configure(state="disabled")

    # ═══════════════════════════════════════
    #   PANEL 1 — MERGE SORT
    # ═══════════════════════════════════════
    def _panel_merge(self, parent):
        p = tk.Frame(parent, bg=BG)
        hdr = tk.Frame(p, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16,4))
        tk.Label(hdr, text="Merge Sort Array",
                 bg=BG, fg=TEXT, font=("Helvetica",16,"bold")).pack(side="left")
        tk.Label(hdr, text="  Virtual Sublists + Single tmpArray  |  Stable  |  O(n log n)",
                 bg=BG, fg=TEXT_DIM, font=("Helvetica",9)).pack(side="left",pady=4)

        # Stats
        sf = tk.Frame(p, bg=BG); sf.pack(fill="x", padx=20, pady=4)
        self.m_comp_f, self.m_comp_v = self._stat_card(sf, "Perbandingan")
        self.m_copy_f, self.m_copy_v = self._stat_card(sf, "Operasi Copy")
        self.m_dep_f,  self.m_dep_v  = self._stat_card(sf, "Kedalaman Rekursi")
        for f in (self.m_comp_f, self.m_copy_f, self.m_dep_f):
            f.pack(side="left", padx=4, ipadx=12, ipady=4)

        # Controls
        cf = tk.Frame(p, bg=BG); cf.pack(fill="x", padx=20, pady=6)
        self.m_entry = tk.Entry(cf, bg=CARD, fg=TEXT, insertbackground=TEXT,
                                font=("Courier",11), relief="flat",
                                highlightbackground=BORDER, highlightthickness=1,
                                width=38)
        self.m_entry.insert(0, "38 27 43 3 9 82 10 18 55 21")
        self.m_entry.pack(side="left", ipady=4, padx=(0,8))
        tk.Button(cf, text="▶  Sort", bg=ACCENT, fg="#fff",
                  font=("Helvetica",10,"bold"), relief="flat", padx=10, pady=4,
                  activebackground="#0F6E56", activeforeground="#fff",
                  command=self._run_merge).pack(side="left", padx=2)
        tk.Button(cf, text="🎲 Acak", bg=CARD, fg=TEXT,
                  relief="flat", padx=8, pady=4,
                  command=self._merge_random).pack(side="left", padx=2)

        # Figure
        self.m_fig, self.m_ax = self._make_fig(3.0)
        self.m_canvas = self._embed_fig(self.m_fig, p)
        self.m_canvas.get_tk_widget().pack(fill="x", padx=20, pady=4)

        # Log
        lf, self.m_log = self._log_widget(p)
        lf.pack(fill="x", padx=20, pady=(0,12))

        self._merge_draw([38,27,43,3,9,82,10,18,55,21], [])
        return p

    def _merge_random(self):
        vals = [random.randint(5, 95) for _ in range(10)]
        self.m_entry.delete(0, "end")
        self.m_entry.insert(0, " ".join(map(str, vals)))

    def _merge_draw(self, arr, hi):
        self.m_ax.clear()
        self.m_ax.set_facecolor(PLT_AX)
        mx = max(arr) if arr else 1
        colors = [ACCENT if i in hi else ACCENT2 for i in range(len(arr))]
        bars = self.m_ax.bar(range(len(arr)), arr, color=colors,
                             edgecolor=BG, linewidth=0.5)
        for bar, v in zip(bars, arr):
            self.m_ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + mx*0.01,
                           str(v), ha="center", va="bottom",
                           color=TEXT, fontsize=8)
        self.m_ax.set_xlim(-0.5, len(arr)-0.5)
        self.m_ax.set_ylim(0, mx * 1.15)
        self.m_ax.set_xticks(range(len(arr)))
        self.m_ax.tick_params(colors=TEXT_DIM, labelsize=8)
        for sp in self.m_ax.spines.values(): sp.set_edgecolor(BORDER)
        self.m_fig.tight_layout()
        self.m_canvas.draw()

    def _run_merge(self):
        try:
            arr = list(map(int, self.m_entry.get().split()))
        except ValueError:
            messagebox.showerror("Input Error", "Masukkan angka integer dipisah spasi")
            return
        self._clear_log(self.m_log)
        sorter = MergeSorter(arr)
        sorter.sort()

        self.m_comp_v.config(text=str(sorter.comparisons))
        self.m_copy_v.config(text=str(sorter.copies))
        self.m_dep_v.config(text=str(sorter.max_depth))

        self._log(self.m_log, f"Input:  {arr}", "dim")
        # animate steps
        def animate(idx):
            if idx >= len(sorter.steps):
                self._merge_draw(sorter.arr, list(range(len(sorter.arr))))
                self._log(self.m_log, f"✓ Output: {sorter.arr}", "ok")
                return
            snap, hi, label = sorter.steps[idx]
            self._merge_draw(snap, hi)
            self._log(self.m_log, label, "info")
            self.after(max(40, 500 - len(arr)*10), lambda: animate(idx+1))
        animate(0)

    # ═══════════════════════════════════════
    #   PANEL 2 — LINKED LIST
    # ═══════════════════════════════════════
    def _panel_ll(self, parent):
        p = tk.Frame(parent, bg=BG)
        hdr = tk.Frame(p, bg=BG); hdr.pack(fill="x", padx=20, pady=(16,4))
        tk.Label(hdr, text="Linked List Merge Sort",
                 bg=BG, fg=TEXT, font=("Helvetica",16,"bold")).pack(side="left")
        tk.Label(hdr, text="  Fast-Slow Pointer + Dummy Node  |  Stable  |  O(log n) space",
                 bg=BG, fg=TEXT_DIM, font=("Helvetica",9)).pack(side="left",pady=4)

        cf = tk.Frame(p, bg=BG); cf.pack(fill="x", padx=20, pady=6)
        self.ll_entry = tk.Entry(cf, bg=CARD, fg=TEXT, insertbackground=TEXT,
                                 font=("Courier",11), relief="flat",
                                 highlightbackground=BORDER, highlightthickness=1, width=38)
        self.ll_entry.insert(0, "5 2 8 1 9 3 7 6")
        self.ll_entry.pack(side="left", ipady=4, padx=(0,8))
        tk.Button(cf, text="▶  Sort", bg=ACCENT, fg="#fff",
                  font=("Helvetica",10,"bold"), relief="flat", padx=10, pady=4,
                  activebackground="#0F6E56", activeforeground="#fff",
                  command=self._run_ll).pack(side="left", padx=2)
        tk.Button(cf, text="🎲 Acak", bg=CARD, fg=TEXT, relief="flat",
                  padx=8, pady=4, command=self._ll_random).pack(side="left", padx=2)

        tk.Label(p, text="List asli:", bg=BG, fg=TEXT_DIM,
                 font=("Helvetica",9)).pack(anchor="w", padx=22, pady=(8,0))
        self.ll_fig1, self.ll_ax1 = self._make_fig(1.6)
        self.ll_c1 = self._embed_fig(self.ll_fig1, p)
        self.ll_c1.get_tk_widget().pack(fill="x", padx=20)

        tk.Label(p, text="Setelah sort:", bg=BG, fg=TEXT_DIM,
                 font=("Helvetica",9)).pack(anchor="w", padx=22, pady=(8,0))
        self.ll_fig2, self.ll_ax2 = self._make_fig(1.6)
        self.ll_c2 = self._embed_fig(self.ll_fig2, p)
        self.ll_c2.get_tk_widget().pack(fill="x", padx=20)

        lf, self.ll_log = self._log_widget(p)
        lf.pack(fill="x", padx=20, pady=8)

        self._ll_draw([5,2,8,1,9,3,7,6], self.ll_ax1, self.ll_fig1, self.ll_c1, ACCENT2)
        return p

    def _ll_random(self):
        vals = [random.randint(1, 50) for _ in range(8)]
        self.ll_entry.delete(0, "end")
        self.ll_entry.insert(0, " ".join(map(str, vals)))

    def _ll_draw(self, arr, ax, fig, canvas, color):
        ax.clear(); ax.set_facecolor(PLT_AX)
        ax.set_xlim(-0.5, max(len(arr)*1.2, 1))
        ax.set_ylim(-0.5, 1.0)
        ax.axis("off")
        for i, v in enumerate(arr):
            x = i * 1.1
            rect = mpatches.FancyBboxPatch((x-0.35, 0.1), 0.7, 0.6,
                                           boxstyle="round,pad=0.04",
                                           facecolor=CARD, edgecolor=color, linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, 0.42, str(v), ha="center", va="center",
                    color=TEXT, fontsize=12, fontweight="bold",
                    fontfamily="monospace")
            ax.text(x, 0.17, f"[{i}]", ha="center", va="center",
                    color=TEXT_DIM, fontsize=8)
            if i < len(arr) - 1:
                ax.annotate("", xy=(x+0.77, 0.42), xytext=(x+0.37, 0.42),
                            arrowprops=dict(arrowstyle="->", color=TEXT_DIM, lw=1.2))
            else:
                ax.text(x+0.42, 0.42, "null", ha="left", va="center",
                        color=TEXT_DIM, fontsize=8)
        fig.tight_layout(); canvas.draw()

    def _run_ll(self):
        try:
            arr = list(map(int, self.ll_entry.get().split()))
        except ValueError:
            messagebox.showerror("Input Error", "Masukkan angka integer dipisah spasi")
            return
        self._clear_log(self.ll_log)
        self._ll_draw(arr, self.ll_ax1, self.ll_fig1, self.ll_c1, ACCENT2)
        sorter = LinkedListSorter(arr)
        sorted_head = sorter.sort()

        # convert back
        result = []
        cur = sorted_head
        while cur:
            result.append(cur.data); cur = cur.next

        self._log(self.ll_log, f"Input:  {arr}", "dim")
        split_cnt = sum(1 for s in sorter.steps if s[0]=="split")
        merge_cnt = sum(1 for s in sorter.steps if s[0]=="merge")
        self._log(self.ll_log, f"Split dilakukan: {split_cnt}x  |  Merge: {merge_cnt}x", "info")
        self._log(self.ll_log, f"✓ Output: {result}", "ok")

        self._ll_draw(result, self.ll_ax2, self.ll_fig2, self.ll_c2, ACCENT)

    # ═══════════════════════════════════════
    #   PANEL 3 — QUICK SORT
    # ═══════════════════════════════════════
    def _panel_quick(self, parent):
        p = tk.Frame(parent, bg=BG)
        hdr = tk.Frame(p, bg=BG); hdr.pack(fill="x", padx=20, pady=(16,4))
        tk.Label(hdr, text="Quick Sort",
                 bg=BG, fg=TEXT, font=("Helvetica",16,"bold")).pack(side="left")
        tk.Label(hdr, text="  Median-of-Three Pivot  |  O(n log n) avg  |  O(n²) worst",
                 bg=BG, fg=TEXT_DIM, font=("Helvetica",9)).pack(side="left",pady=4)

        sf = tk.Frame(p, bg=BG); sf.pack(fill="x", padx=20, pady=4)
        self.q_comp_f, self.q_comp_v = self._stat_card(sf, "Perbandingan")
        self.q_dep_f,  self.q_dep_v  = self._stat_card(sf, "Max Rekursi")
        self.q_piv_f,  self.q_piv_v  = self._stat_card(sf, "Pivot Terakhir")
        for f in (self.q_comp_f, self.q_dep_f, self.q_piv_f):
            f.pack(side="left", padx=4, ipadx=12, ipady=4)

        cf = tk.Frame(p, bg=BG); cf.pack(fill="x", padx=20, pady=6)
        self.q_entry = tk.Entry(cf, bg=CARD, fg=TEXT, insertbackground=TEXT,
                                font=("Courier",11), relief="flat",
                                highlightbackground=BORDER, highlightthickness=1, width=32)
        self.q_entry.insert(0, "64 34 25 12 22 11 90 3 45 77")
        self.q_entry.pack(side="left", ipady=4, padx=(0,8))
        tk.Button(cf, text="▶  Sort", bg=ACCENT, fg="#fff",
                  font=("Helvetica",10,"bold"), relief="flat", padx=10, pady=4,
                  activebackground="#0F6E56", activeforeground="#fff",
                  command=self._run_quick).pack(side="left", padx=2)
        tk.Button(cf, text="⬇ Descending (Worst)", bg=ACCENT3, fg="#fff",
                  relief="flat", padx=8, pady=4,
                  command=self._quick_desc).pack(side="left", padx=2)
        tk.Button(cf, text="🎲 Acak", bg=CARD, fg=TEXT, relief="flat",
                  padx=8, pady=4, command=self._quick_random).pack(side="left", padx=2)

        self.q_fig, self.q_ax = self._make_fig(3.0)
        self.q_canvas = self._embed_fig(self.q_fig, p)
        self.q_canvas.get_tk_widget().pack(fill="x", padx=20, pady=4)

        lf, self.q_log = self._log_widget(p)
        lf.pack(fill="x", padx=20, pady=(0,12))

        self._quick_draw([64,34,25,12,22,11,90,3,45,77], -1, -1, -1, [])
        return p

    def _quick_random(self):
        vals = [random.randint(5, 95) for _ in range(10)]
        self.q_entry.delete(0, "end")
        self.q_entry.insert(0, " ".join(map(str, vals)))

    def _quick_desc(self):
        vals = sorted([random.randint(5,95) for _ in range(10)], reverse=True)
        self.q_entry.delete(0, "end")
        self.q_entry.insert(0, " ".join(map(str, vals)))

    def _quick_draw(self, arr, pivot_pos, lo, hi, sorted_set):
        self.q_ax.clear(); self.q_ax.set_facecolor(PLT_AX)
        mx = max(arr) if arr else 1
        colors = []
        for i in range(len(arr)):
            if i in sorted_set:   colors.append(ACCENT)
            elif i == pivot_pos:  colors.append(ACCENT3)
            elif lo <= i <= hi:   colors.append(ACCENT4)
            else:                 colors.append(ACCENT2)
        bars = self.q_ax.bar(range(len(arr)), arr, color=colors,
                             edgecolor=BG, linewidth=0.5)
        for bar, v in zip(bars, arr):
            self.q_ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + mx*0.01,
                           str(v), ha="center", va="bottom", color=TEXT, fontsize=8)
        self.q_ax.set_xlim(-0.5, len(arr)-0.5)
        self.q_ax.set_ylim(0, mx * 1.15)
        self.q_ax.tick_params(colors=TEXT_DIM, labelsize=8)
        for sp in self.q_ax.spines.values(): sp.set_edgecolor(BORDER)
        # legend
        legend_elems = [
            mpatches.Patch(color=ACCENT3, label="Pivot"),
            mpatches.Patch(color=ACCENT4, label="Partisi aktif"),
            mpatches.Patch(color=ACCENT2, label="Belum diproses"),
            mpatches.Patch(color=ACCENT,  label="Terurut"),
        ]
        self.q_ax.legend(handles=legend_elems, loc="upper right",
                         facecolor=CARD, edgecolor=BORDER,
                         labelcolor=TEXT, fontsize=8)
        self.q_fig.tight_layout(); self.q_canvas.draw()

    def _run_quick(self):
        try:
            arr = list(map(int, self.q_entry.get().split()))
        except ValueError:
            messagebox.showerror("Input Error", "Masukkan angka integer dipisah spasi")
            return
        self._clear_log(self.q_log)
        sorter = QuickSorter(arr)
        sorter.sort()

        self.q_comp_v.config(text=str(sorter.comparisons))
        self.q_dep_v.config(text=str(sorter.max_depth))

        self._log(self.q_log, f"Input: {arr}", "dim")
        sorted_set = set()

        def animate(idx):
            if idx >= len(sorter.steps):
                self._quick_draw(sorter.arr, -1, -1, -1,
                                 set(range(len(sorter.arr))))
                self._log(self.q_log, f"✓ Output: {sorter.arr}", "ok")
                return
            snap, pivot_pos, lo, hi, label = sorter.steps[idx]
            sorted_set.add(pivot_pos)
            self.q_piv_v.config(text=str(snap[pivot_pos]))
            self._quick_draw(snap, pivot_pos, lo, hi, sorted_set.copy())
            self._log(self.q_log, label, "pivot")
            self.after(max(50, 600 - len(arr)*15), lambda: animate(idx+1))

        animate(0)

    # ═══════════════════════════════════════
    #   PANEL 4 — EXPRESSION TREE
    # ═══════════════════════════════════════
    def _panel_expr(self, parent):
        p = tk.Frame(parent, bg=BG)
        hdr = tk.Frame(p, bg=BG); hdr.pack(fill="x", padx=20, pady=(16,4))
        tk.Label(hdr, text="Expression Tree Builder",
                 bg=BG, fg=TEXT, font=("Helvetica",16,"bold")).pack(side="left")
        tk.Label(hdr, text="  Rekursi + Postorder Traversal",
                 bg=BG, fg=TEXT_DIM, font=("Helvetica",9)).pack(side="left",pady=4)

        cf = tk.Frame(p, bg=BG); cf.pack(fill="x", padx=20, pady=6)
        tk.Label(cf, text="Ekspresi:", bg=BG, fg=TEXT_DIM,
                 font=("Helvetica",10)).pack(side="left", padx=(0,6))
        self.expr_entry = tk.Entry(cf, bg=CARD, fg=TEXT, insertbackground=TEXT,
                                   font=("Courier",11), relief="flat",
                                   highlightbackground=BORDER, highlightthickness=1, width=38)
        self.expr_entry.insert(0, "((8*5)+(9/(7-4)))")
        self.expr_entry.pack(side="left", ipady=4, padx=(0,8))
        tk.Button(cf, text="▶  Bangun", bg=ACCENT, fg="#fff",
                  font=("Helvetica",10,"bold"), relief="flat", padx=10, pady=4,
                  activebackground="#0F6E56", activeforeground="#fff",
                  command=self._run_expr).pack(side="left", padx=2)

        rf = tk.Frame(p, bg=BG); rf.pack(fill="x", padx=20, pady=4)
        self.expr_result_f, self.expr_result_v = self._stat_card(rf, "Hasil Evaluasi")
        self.expr_result_f.pack(side="left", padx=4, ipadx=16, ipady=4)
        pf = tk.Frame(rf, bg=CARD,
                      highlightbackground=BORDER, highlightthickness=1)
        pf.pack(side="left", padx=4, ipadx=8, ipady=4)
        tk.Label(pf, text="Notasi Postfix:", bg=CARD, fg=TEXT_DIM,
                 font=("Helvetica",9)).pack(anchor="w", padx=8, pady=(6,0))
        self.expr_postfix_v = tk.Label(pf, text="—",
                                       bg=CARD, fg=ACCENT4,
                                       font=("Courier",10,"bold"))
        self.expr_postfix_v.pack(padx=8, pady=(0,6))

        self.expr_fig, self.expr_ax = self._make_fig(3.6)
        self.expr_canvas = self._embed_fig(self.expr_fig, p)
        self.expr_canvas.get_tk_widget().pack(fill="x", padx=20, pady=4)

        lf, self.expr_log = self._log_widget(p)
        lf.pack(fill="x", padx=20, pady=(0,12))

        self._run_expr()
        return p

    def _draw_node(self, ax, node, parent_xy=None):
        if not node: return
        x, y = node.x, node.y * 1.4
        if parent_xy:
            ax.plot([parent_xy[0], x], [parent_xy[1], y],
                    color=BORDER, lw=1.5, zorder=1)
        is_op = node.val in "+-*/"
        color = PURPLE if is_op else ACCENT
        circle = plt.Circle((x, y), 0.28,
                             facecolor=CARD, edgecolor=color,
                             linewidth=2, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, node.val, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color,
                fontfamily="monospace", zorder=3)
        self._draw_node(ax, node.left,  (x, y))
        self._draw_node(ax, node.right, (x, y))

    def _run_expr(self):
        expr = self.expr_entry.get().replace(" ", "")
        self._clear_log(self.expr_log)
        try:
            tree = ExprTree(expr)
            tree.build()
        except Exception as e:
            messagebox.showerror("Parse Error", str(e))
            return

        res = tree.result
        self.expr_result_v.config(
            text=str(int(res)) if isinstance(res, float) and res.is_integer() else f"{res:.3f}")
        self.expr_postfix_v.config(text="  ".join(tree.postfix))

        self.expr_ax.clear(); self.expr_ax.set_facecolor(PLT_AX)
        self.expr_ax.set_aspect("equal")
        self.expr_ax.axis("off")
        self._draw_node(self.expr_ax, tree.root)
        self.expr_ax.autoscale_view()
        self.expr_fig.tight_layout(); self.expr_canvas.draw()

        self._log(self.expr_log, f"Ekspresi: {expr}", "dim")
        self._log(self.expr_log, f"Postorder: {' → '.join(tree.postfix)}", "info")
        self._log(self.expr_log, f"Hasil evaluasi: {res}", "ok")

    # ═══════════════════════════════════════
    #   PANEL 5 — HEAP SORT
    # ═══════════════════════════════════════
    def _panel_heap(self, parent):
        p = tk.Frame(parent, bg=BG)
        hdr = tk.Frame(p, bg=BG); hdr.pack(fill="x", padx=20, pady=(16,4))
        tk.Label(hdr, text="In-Place Heap Sort",
                 bg=BG, fg=TEXT, font=("Helvetica",16,"bold")).pack(side="left")
        tk.Label(hdr, text="  Max-Heap + Sift-Down  |  O(n log n)  |  O(1) extra space",
                 bg=BG, fg=TEXT_DIM, font=("Helvetica",9)).pack(side="left",pady=4)

        sf = tk.Frame(p, bg=BG); sf.pack(fill="x", padx=20, pady=4)
        self.h_comp_f, self.h_comp_v = self._stat_card(sf, "Perbandingan")
        self.h_swap_f, self.h_swap_v = self._stat_card(sf, "Swap")
        self.h_phase_f,self.h_phase_v = self._stat_card(sf, "Fase")
        for f in (self.h_comp_f, self.h_swap_f, self.h_phase_f):
            f.pack(side="left", padx=4, ipadx=12, ipady=4)

        cf = tk.Frame(p, bg=BG); cf.pack(fill="x", padx=20, pady=6)
        self.h_entry = tk.Entry(cf, bg=CARD, fg=TEXT, insertbackground=TEXT,
                                font=("Courier",11), relief="flat",
                                highlightbackground=BORDER, highlightthickness=1, width=36)
        self.h_entry.insert(0, "42 17 8 31 65 23 11 55")
        self.h_entry.pack(side="left", ipady=4, padx=(0,8))
        tk.Button(cf, text="▶  Sort", bg=ACCENT, fg="#fff",
                  font=("Helvetica",10,"bold"), relief="flat", padx=10, pady=4,
                  activebackground="#0F6E56", activeforeground="#fff",
                  command=self._run_heap).pack(side="left", padx=2)
        tk.Button(cf, text="🎲 Acak", bg=CARD, fg=TEXT, relief="flat",
                  padx=8, pady=4, command=self._heap_random).pack(side="left", padx=2)

        # Two subplots: array bar + tree
        self.h_fig = plt.figure(figsize=(8, 4.0), facecolor=PLT_BG)
        self.h_ax_bar  = self.h_fig.add_subplot(121, facecolor=PLT_AX)
        self.h_ax_tree = self.h_fig.add_subplot(122, facecolor=PLT_AX)
        self.h_canvas  = self._embed_fig(self.h_fig, p)
        self.h_canvas.get_tk_widget().pack(fill="x", padx=20, pady=4)

        lf, self.h_log = self._log_widget(p)
        lf.pack(fill="x", padx=20, pady=(0,12))

        self._heap_draw([42,17,8,31,65,23,11,55], len([42,17,8,31,65,23,11,55]), [], "—")
        return p

    def _heap_random(self):
        vals = [random.randint(5, 95) for _ in range(8)]
        self.h_entry.delete(0, "end")
        self.h_entry.insert(0, " ".join(map(str, vals)))

    def _heap_draw(self, arr, heap_size, hi_pair, phase):
        for ax in (self.h_ax_bar, self.h_ax_tree):
            ax.clear(); ax.set_facecolor(PLT_AX)

        # Bar chart
        colors = []
        for i in range(len(arr)):
            if i >= heap_size: colors.append(ACCENT)
            elif i in hi_pair: colors.append(ACCENT3)
            else:              colors.append(ACCENT2)
        mx = max(arr) if arr else 1
        bars = self.h_ax_bar.bar(range(len(arr)), arr, color=colors,
                                 edgecolor=BG, linewidth=0.5)
        for bar, v in zip(bars, arr):
            self.h_ax_bar.text(bar.get_x()+bar.get_width()/2,
                               bar.get_height()+mx*0.01,
                               str(v), ha="center", va="bottom",
                               color=TEXT, fontsize=8)
        self.h_ax_bar.set_xlim(-0.5, len(arr)-0.5)
        self.h_ax_bar.set_ylim(0, mx*1.15)
        self.h_ax_bar.tick_params(colors=TEXT_DIM, labelsize=7)
        for sp in self.h_ax_bar.spines.values(): sp.set_edgecolor(BORDER)
        self.h_ax_bar.set_title("Array", color=TEXT_DIM, fontsize=9)

        # Tree
        self.h_ax_tree.axis("off")
        n = heap_size
        if n > 0:
            def pos(i):
                d = int(math.log2(i+1))
                p = i - (2**d - 1)
                total = 2**d
                return p/total + 0.5/total, -(d * 0.7)

            for i in range(n):
                x, y = pos(i)
                l, r = 2*i+1, 2*i+2
                if l < n:
                    xl, yl = pos(l)
                    self.h_ax_tree.plot([x, xl], [y, yl],
                                       color=BORDER, lw=1.2, zorder=1)
                if r < n:
                    xr, yr = pos(r)
                    self.h_ax_tree.plot([x, xr], [y, yr],
                                       color=BORDER, lw=1.2, zorder=1)

            for i in range(n):
                x, y = pos(i)
                ec = ACCENT3 if i in hi_pair else (ACCENT if i==0 else ACCENT2)
                circle = plt.Circle((x, y), 0.04,
                                    facecolor=CARD, edgecolor=ec,
                                    linewidth=1.5, zorder=2,
                                    transform=self.h_ax_tree.transData)
                self.h_ax_tree.add_patch(circle)
                self.h_ax_tree.text(x, y, str(arr[i]),
                                    ha="center", va="center",
                                    fontsize=9, fontweight="bold",
                                    color=ec, fontfamily="monospace", zorder=3)

        self.h_ax_tree.set_xlim(-0.05, 1.05)
        self.h_ax_tree.set_ylim(-2.5, 0.2)
        self.h_ax_tree.set_title(f"Heap Tree  [{phase}]",
                                 color=TEXT_DIM, fontsize=9)
        self.h_fig.tight_layout(); self.h_canvas.draw()

    def _run_heap(self):
        try:
            arr = list(map(int, self.h_entry.get().split()))
        except ValueError:
            messagebox.showerror("Input Error", "Masukkan angka integer dipisah spasi")
            return
        self._clear_log(self.h_log)
        sorter = HeapSorter(arr)
        sorter.sort()

        self.h_comp_v.config(text=str(sorter.comparisons))
        self.h_swap_v.config(text=str(sorter.swaps))

        self._log(self.h_log, f"Input: {arr}", "dim")

        def animate(idx):
            if idx >= len(sorter.steps):
                self._heap_draw(sorter.arr, 1, [], "Done ✓")
                self.h_phase_v.config(text="Done ✓")
                self._log(self.h_log, f"✓ Output: {sorter.arr}", "ok")
                return
            snap, hs, pair, phase = sorter.steps[idx]
            self.h_phase_v.config(text=phase)
            self._heap_draw(snap, hs, list(pair), phase)
            if "Extract" in phase:
                self._log(self.h_log, phase, "warn")
            else:
                self._log(self.h_log, phase, "info")
            self.after(max(60, 500 - len(arr)*10), lambda: animate(idx+1))

        animate(0)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
