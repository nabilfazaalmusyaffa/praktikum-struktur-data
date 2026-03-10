<<<<<<< HEAD
=======
<<<<<<< HEAD
🧠 Praktikum Struktur Data
📂 Rincian Implementasi ProgramProyek ini mencakup berbagai implementasi struktur data dan algoritma yang disusun secara modular. Dimulai dari aspek fundamental, file array.py menyajikan implementasi Abstract Data Type (ADT) Array dengan ukuran tetap yang memanfaatkan magic methods Python seperti __getitem__ dan __setitem__ untuk validasi indeks yang ketat. Pada sisi simulasi, terdapat game_of_life.py yang menerapkan Conway’s Game of Life menggunakan manipulasi grid 2D dan logika transisi sel otomatis. Untuk manajemen data sederhana, simulasi buku telepon.py mendemonstrasikan penyimpanan kontak berbasis list dengan fitur Linear Search, sementara modified binary search.py menawarkan solusi pencarian yang lebih efisien dengan kompleksitas $O(\log n)$ yang telah disesuaikan untuk menangani kondisi data khusus.Dalam kategori algoritma pengurutan dan manipulasi list, repositori ini menyediakan bubble_sort.py yang dilengkapi dengan visualisasi langkah demi langkah untuk mempermudah pemahaman alur $O(n^2)$, serta hybrid_sort.py yang menggabungkan efisiensi Merge Sort dan Insertion Sort. Terdapat juga merge tiga sorted list.py yang mengoptimalkan penggabungan tiga sumber data terurut menjadi satu kesatuan. Untuk analisis data, file inversion counter.py digunakan untuk mengukur tingkat keacakan array, sedangkan deduplikasi.py dan first_recurring_character.py berfungsi untuk mengelola elemen duplikat dan menemukan repetisi pertama dalam sekumpulan data. Terakhir, proyek ini dilengkapi dengan alat pembanding seperti anagram check.py untuk validasi kemiripan string dan intersection dua array.py untuk menemukan irisan elemen di antara dua struktur data berbeda.

ADT Array & Conway’s Game of Life Simulation in Python


📌 Project Overview

Project ini merupakan implementasi:

✅ Abstract Data Type (ADT) Array

✅ Simulasi Conway’s Game of Life

✅ Konsep OOP (Object-Oriented Programming)

✅ Manipulasi Grid 2D

✅ Deep Copy & Iterasi

Project dibuat sebagai bagian dari praktikum mata kuliah Struktur Data.

📂 Project Structure
praktikum-struktur-data/
│
├── array.py          # Implementasi ADT Array
├── game_of_life.py   # Simulasi Game of Life
└── README.md         # Dokumentasi project

🧩 1️⃣ ADT Array Implementation
📖 Deskripsi

Kelas Array merupakan implementasi array dengan ukuran tetap (fixed size) yang memiliki fitur:

Konstruktor validasi ukuran

Akses index dengan validasi

Modifikasi elemen

Clear semua elemen

Support iterasi dengan __iter__

Mendukung fungsi len()

⚙️ Method Overview
Method	Fungsi
__init__(size)	Membuat array dengan ukuran tetap
__len__()	Mengembalikan panjang array
__getitem__(index)	Mengambil nilai berdasarkan index
__setitem__(index, value)	Mengubah nilai pada index
clear(value)	Mengisi seluruh array dengan nilai tertentu
__iter__()	Agar bisa digunakan dalam perulangan
💻 Contoh Output ADT Array
Panjang array: 5

Isi array setelah diisi:
10
20
30
None
None

Nilai pada index 1: 20

Isi array setelah clear:
0
0
0
0
0

🎮 2️⃣ Conway’s Game of Life
📖 Deskripsi

Game of Life adalah simulasi otomatis berbasis grid 2D yang mengikuti aturan matematika sederhana untuk menentukan apakah sel hidup atau mati di generasi berikutnya.

Ukuran grid: 5 x 5
Jumlah generasi: 5
Delay antar generasi: 1 detik

📜 Aturan Game of Life

Sel hidup dengan < 2 tetangga → mati (Underpopulation)

Sel hidup dengan 2 atau 3 tetangga → tetap hidup

Sel hidup dengan > 3 tetangga → mati (Overpopulation)

Sel mati dengan tepat 3 tetangga → menjadi hidup (Reproduction)

🖥 Contoh Tampilan di Terminal
Generasi: 0
. . . . .
. ■ ■ ■ .
. . ■ . .
. . . . .
. . . . .

Generasi: 1
. . ■ . .
. . ■ . .
. ■ ■ . .
. . . . .
. . . . .


(Simulasi terus berjalan hingga generasi ke-4)

▶️ Cara Menjalankan Project
1️⃣ Clone Repository
git clone https://github.com/USERNAME/praktikum-struktur-data.git

2️⃣ Masuk ke Folder
cd praktikum-struktur-data

3️⃣ Jalankan Program

Untuk ADT Array:

python array.py


Untuk Game of Life:

python game_of_life.py

🛠 Technologies Used

Python 3

Object-Oriented Programming

Deep Copy (copy.deepcopy)

Time Delay (time.sleep)

2D Grid Iteration

🎯 Learning Objectives


Memahami konsep Abstract Data Type (ADT)

Mengimplementasikan array dengan ukuran tetap

Menggunakan method khusus Python (__len__, __getitem__, dll)

Mengimplementasikan simulasi berbasis aturan matematis

Melatih logika dan pemodelan sistem

👨‍💻 Author

Nabil Faza
Mahasiswa Manajemen Informatika
Praktikum Struktur Data
=======
>>>>>>> 7d212e4
# 🎮 Game of Life – Implementasi Array 2D

## 📌 Deskripsi
Program ini merupakan simulasi Game of Life yang diperkenalkan oleh matematikawan Inggris, John Conway. 
Simulasi ini menggunakan struktur data Array 2 dimensi (list di dalam list) untuk merepresentasikan sel hidup dan sel mati.

## 🧠 Konsep Struktur Data
- Menggunakan array 2D (matrix)
- Nilai 1 = Sel hidup
- Nilai 0 = Sel mati
- Iterasi digunakan untuk menghitung tetangga setiap sel
- Array baru dibuat untuk menyimpan generasi berikutnya

## ⚙️ Aturan Game
1. Sel hidup dengan kurang dari 2 tetangga → mati
2. Sel hidup dengan 2 atau 3 tetangga → tetap hidup
3. Sel hidup dengan lebih dari 3 tetangga → mati
4. Sel mati dengan tepat 3 tetangga → hidup

## 📂 Struktur Folder

## 📊 Contoh Output
Simulasi akan menampilkan grid dengan simbol:
■ = Sel hidup  
. = Sel mati

## 👨‍💻 Dibuat untuk Tugas Struktur Data
Prodi Manajemen Informatika

<<<<<<< HEAD
==============================================
==============================================
=======
>>>>>>> 7d212e4

# 📞 Simulasi Buku Telepon – Implementasi Array

## 📌 Deskripsi
Program ini merupakan simulasi sederhana buku telepon menggunakan struktur data Array (List).
Data disimpan dalam bentuk list yang berisi [nama, nomor telepon].

## 🧠 Konsep Struktur Data
- Menggunakan array (list)
- Operasi dasar:
  - Tambah data (append)
  - Tampilkan data (perulangan)
  - Cari data (linear search)

## 📂 Struktur Folder

## ▶️ Cara Menjalankan
1. Pastikan Python sudah terinstall
2. Jalankan perintah:

## 📋 Menu Program
1. Tambah kontak
2. Tampilkan kontak
3. Cari kontak
4. Keluar

## 👨‍💻 Dibuat untuk Tugas Struktur Data
<<<<<<< HEAD
Prodi Manajemen Informatika
=======
Prodi Manajemen Informatika
>>>>>>> d8a51a7 (Tambah README)
>>>>>>> 7d212e4
