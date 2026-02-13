🧠 Praktikum Struktur Data
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
