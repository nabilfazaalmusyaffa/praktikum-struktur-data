# 🧠 Praktikum Struktur Data

## 📌 Project Overview

## 📄 Laporan Tugas Queue

Laporan ini berisi pembahasan tentang struktur data Queue, termasuk analisis dan implementasi.

[📥 Lihat / Download Laporan Queue](./laporan_queue.pdf)
Proyek ini berisi berbagai implementasi struktur data dan algoritma menggunakan Python, mulai dari konsep dasar hingga simulasi dan optimasi algoritma.

Project dibuat sebagai bagian dari praktikum mata kuliah Struktur Data.

---

## 📂 Project Structure

praktikum-struktur-data/
│
├── array.py                     # Implementasi ADT Array
├── game_of_life.py              # Simulasi Game of Life
├── buku_telepon.py              # Simulasi Buku Telepon
├── modified_binary_search.py    # Binary Search Modifikasi
├── bubble_sort.py               # Bubble Sort (visualisasi)
├── hybrid_sort.py               # Hybrid Merge + Insertion Sort
├── merge_tiga_sorted_list.py    # Merge 3 list terurut
├── inversion_counter.py         # Hitung tingkat keacakan array
├── deduplikasi.py               # Hapus duplikat
├── first_recurring_character.py # Cari karakter berulang pertama
├── anagram_check.py             # Cek anagram
├── intersection_dua_array.py    # Irisan dua array
├── biginteger.py                # Operasi bilangan besar (Big Integer)
├── labirin maze.py              # Simulasi dan penyelesaian labirin (Maze)
├── python_queue_simulation.py   # Simulasi Queue (FIFO & kasus nyata)
└── README.md

---

## 🧩 1️⃣ ADT Array

Implementasi array dengan ukuran tetap (fixed size).

### Fitur:

* Validasi index
* Akses & modifikasi data
* Iterasi (**iter**)
* Fungsi len()
* Clear array

---

## 🎮 2️⃣ Conway’s Game of Life

Simulasi grid 2D berbasis aturan matematika.

### Aturan:

* < 2 tetangga → mati
* 2–3 tetangga → hidup
* > 3 tetangga → mati
* Tepat 3 → hidup

---

## 📞 3️⃣ Simulasi Buku Telepon

Implementasi sederhana menggunakan array (list).

### Fitur:

* Tambah kontak
* Tampilkan kontak
* Cari kontak (Linear Search)

---

## 🔍 4️⃣ Algoritma Pencarian & Sorting

* Binary Search (O(log n))
* Bubble Sort (O(n²))
* Hybrid Sort (Merge + Insertion)
* Merge 3 Sorted List

---

## 📊 5️⃣ Analisis Data

* Inversion Counter
* Deduplikasi
* First Recurring Character
* Intersection Array

---

## 🔢 6️⃣ Big Integer (Bilangan Besar)

File `biginteger.py` digunakan untuk menangani operasi bilangan dengan digit sangat besar yang tidak dapat ditangani oleh tipe data integer biasa.

### Fitur:

* Penjumlahan bilangan besar
* Pengurangan bilangan besar
* Representasi angka dalam bentuk string
* Simulasi perhitungan manual (digit per digit)

---

## 🗺️ 7️⃣ Simulasi Labirin (Maze)

File `labirin maze.py` berisi program untuk membuat grid labirin 2D dan mencari jalan keluar (pathfinding).

### Fitur:

* Build Maze
* Visualisasi labirin
* Pencarian jalur (pathfinding)

---

## 🔄 8️⃣ Simulasi Queue (FIFO & Kasus Nyata)

File `python_queue_simulation.py` berisi implementasi dan simulasi konsep Queue (antrian) menggunakan prinsip FIFO (First In First Out).

### Kasus yang Disimulasikan:

1. 🖨️ Antrian Printer

   * Dokumen masuk dan diproses sesuai urutan

2. 🎮 Hot Potato (Circular Queue)

   * Simulasi permainan dengan eliminasi pemain

3. 🏥 Antrian Rumah Sakit (Priority Queue)

   * Pasien dengan prioritas lebih tinggi dilayani lebih dulu

4. 🌐 Breadth First Search (BFS)

   * Traversal graph menggunakan queue

5. ✈️ Simulasi Loket Bandara

   * Antrian penumpang dan proses pelayanan

### Fitur:

* Visualisasi antrian di terminal
* Proses enqueue dan dequeue
* Animasi sederhana menggunakan delay
* Output step-by-step

### Tujuan:

* Memahami konsep Queue secara praktis
* Melihat implementasi Queue dalam kasus nyata
* Membantu visualisasi proses antrian

---

## ▶️ Cara Menjalankan Project

1. Clone repository:

```bash
git clone https://github.com/nabilfazaalmusyaffa/praktikum-struktur-data.git
```

2. Masuk ke folder:

```bash
cd praktikum-struktur-data
```

3. Jalankan file yang diinginkan:

```bash
python nama_file.py
```

Contoh:

```bash
python python_queue_simulation.py
```

---

## 📎 Kesimpulan

Project ini membantu memahami konsep struktur data melalui implementasi langsung menggunakan Python, mulai dari array hingga simulasi kompleks seperti queue dan maze.

---

## 🙏 Terima Kasih

Terima kasih telah mengunjungi repository ini 🙌
