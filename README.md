# 🧠 Praktikum Struktur Data

## 📌 Project Overview
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
└── README.md

---

## 🧩 1️⃣ ADT Array
Implementasi array dengan ukuran tetap (fixed size).

### Fitur:
- Validasi index
- Akses & modifikasi data
- Iterasi (__iter__)
- Fungsi len()
- Clear array

---

## 🎮 2️⃣ Conway’s Game of Life
Simulasi grid 2D berbasis aturan matematika.

### Aturan:
- < 2 tetangga → mati
- 2–3 tetangga → hidup
- > 3 tetangga → mati
- Tepat 3 → hidup

---

## 📞 3️⃣ Simulasi Buku Telepon
Implementasi sederhana menggunakan array (list).

### Fitur:
- Tambah kontak
- Tampilkan kontak
- Cari kontak (Linear Search)

---

## 🔍 4️⃣ Algoritma Pencarian & Sorting
- Binary Search (O(log n))
- Bubble Sort (O(n²))
- Hybrid Sort (Merge + Insertion)
- Merge 3 Sorted List

---

## 📊 5️⃣ Analisis Data
- Inversion Counter
- Deduplikasi
- First Recurring Character
- Intersection Array

---

## 🔢 6️⃣ Big Integer (Bilangan Besar)
File `biginteger.py` digunakan untuk menangani operasi bilangan dengan digit sangat besar yang tidak dapat ditangani oleh tipe data integer biasa.

### Fitur:
- Penjumlahan bilangan besar
- Pengurangan bilangan besar
- Representasi angka dalam bentuk string
- Simulasi perhitungan manual (digit per digit)

### Tujuan:
- Memahami keterbatasan tipe data bawaan
- Melatih logika manipulasi string & array
- Implementasi konsep matematika dalam pemrograman

---

## ▶️ Cara Menjalankan Project

1. Clone repository:
```bash
git clone https://github.com/USERNAME/praktikum-struktur-data.git