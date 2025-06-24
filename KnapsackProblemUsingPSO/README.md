# Knapsack Problem using PSO (Particle Swarm Optimization)

Aplikasi web Flask untuk menyelesaikan masalah Knapsack menggunakan algoritma Particle Swarm Optimization (PSO).

## Fitur

- Input parameter PSO (kapasitas knapsack, jumlah iterasi, jumlah partikel)
- CRUD data item (tambah, edit, hapus item dengan berat dan nilai)
- Menjalankan algoritma Knapsack PSO
- Menampilkan hasil terbaik (kombinasi item, total berat, total nilai)
- Grafik fitness per generasi

## Cara Menjalankan (Lokal)

### 1. Install Dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python main.py
```

### 3. Akses di Browser
```
http://127.0.0.1:5000/
```

## Cara Deploy ke Cloud

### Railway (Gratis)
1. Daftar di [railway.app](https://railway.app)
2. Upload kode ke GitHub
3. Connect repository ke Railway
4. Railway akan auto-deploy

### Render (Gratis)
1. Daftar di [render.com](https://render.com)
2. Connect GitHub repository
3. Pilih "Web Service"
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python main.py`

### Heroku
1. Daftar di [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Deploy via command line:
```bash
heroku create your-app-name
git push heroku main
```

## Struktur File

```
KnapsackProblemUsingPSO/
├── main.py              # Aplikasi Flask utama
├── KnapsackPSO.py       # Algoritma PSO (jangan diubah)
├── requirements.txt     # Dependensi Python
├── Procfile            # Konfigurasi deployment
├── README.md           # Dokumentasi
└── templates/
    ├── index.html      # Halaman utama
    └── result.html     # Halaman hasil
```

## Penggunaan

1. **Input Parameter PSO**: Masukkan kapasitas knapsack, jumlah iterasi, dan jumlah partikel
2. **Tambah Item**: Input berat dan nilai untuk setiap item
3. **Edit/Hapus Item**: Gunakan tombol edit/hapus di tabel item
4. **Jalankan PSO**: Klik tombol "Jalankan PSO" untuk memulai algoritma
5. **Lihat Hasil**: Hasil terbaik dan grafik fitness akan ditampilkan

## Dependensi

- Flask 2.3.3
- matplotlib 3.7.2
- numpy 1.24.3
- Werkzeug 2.3.7
- Jinja2 3.1.2 