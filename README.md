# Tucil3_13524015_13524066

## Anggota Kelompok

| Nama | NIM |
|---|---|
| Mahatma Brahmana | 13524015 |
| Nathanael Gunawan | 13524066 |

---

## Ice Sliding Puzzle Solver

Program ini dibuat untuk menyelesaikan permainan **Ice Sliding Puzzle** menggunakan beberapa algoritma pathfinding. Pada permainan ini, aktor harus bergerak dari titik awal menuju titik tujuan pada papan es. Karena permukaan licin, aktor tidak berhenti setiap satu petak, melainkan terus bergerak sampai tepat sebelum menabrak rintangan.

Program ini mengimplementasikan algoritma:

1. Uniform Cost Search (UCS)
2. Greedy Best First Search (GBFS)
3. A* Search
4. Breadth-First Search (BFS) sebagai algoritma bonus

---

## Deskripsi Singkat

Papan permainan direpresentasikan dalam bentuk matriks. Setiap petak dapat berupa:

| Simbol | Keterangan |
|---|---|
| `Z` | Posisi awal aktor |
| `O` | Titik tujuan |
| `X` | Rintangan/batu |
| `L` | Lava |
| `*` | Petak kosong |
| `0-9` | Checkpoint yang harus dilewati berurutan |

Aktor hanya dapat bergerak ke empat arah, yaitu atas, bawah, kiri, dan kanan. Setelah memilih arah, aktor akan terus meluncur sampai berhenti tepat sebelum rintangan `X`.

Solusi dianggap berhasil jika aktor berhenti tepat di titik tujuan `O` dan seluruh checkpoint telah dilewati sesuai urutan.

---
## Cara Menjalankan
Jalankan langsung dengan Python:

```bash
python src/main.py
```

Jika ingin menambahkan file input, buat atau simpan file tersebut di folder `test/input/`.

---

## Struktur Folder

```txt
Tucil3_13524015_13524066/
├── src/
│   ├── main.py
│   ├── parser.py
│   ├── validator.py
│   ├── board.py
│   ├── movement.py
│   ├── heuristic.py
│   ├── utils.py
│   └── algorithms/
│       ├── bfs.py
│       ├── ucs.py
│       ├── gbfs.py
│       ├── astar.py
│       └── __init__.py
├── test/
│   ├── input/
│   │   ├── input1.txt
│   │   ├── input2.txt
│   │   ├── input3.txt
│   │   ├── input4.txt
│   │   ├── input5.txt
│   │   └── input6.txt
│   └── output/
│       ├── BFS/
│       ├── UCS/
│       ├── GBFS/
│       │   ├── Manhattan/
│       │   ├── Pythagoras/
│       │   ├── Manhattan + Checkpoint Tersisa/
│       │   ├── Manhattan Rantai Checkpoint/
│       │   └── Jarak Minimum Slide/
│       └── ASTAR/
│           ├── Manhattan/
│           ├── Pythagoras/
│           ├── Manhattan + Checkpoint Tersisa/
│           ├── Manhattan Rantai Checkpoint/
│           └── Jarak Minimum Slide/
├── README.md
```
