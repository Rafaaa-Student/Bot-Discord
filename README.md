# Bot Raffasya VII 🌿🤖

Bot Discord interaktif yang menggabungkan **gamifikasi aksi hijau**, **web scraping**, dan **dashboard website** untuk mendorong gaya hidup ramah lingkungan.

---

## 📋 Fitur Utama

### 🌱 Fitur Aksi Hijau (Green Action System)
Bot ini dirancang untuk memotivasi pengguna melakukan tindakan ramah lingkungan dengan sistem poin dan level:

- **$Green_Action**: Dapatkan tips hijau harian + 1 poin (max 3x sehari)
- **$Action <aksi>**: Catat aksi hijau (misal: "Menanam pohon") + 5 poin
- **$Story <cerita>**: Cerita storytelling 30+ kata tentang aktivitas hijau (poin sesuai aksi yang terdeteksi)
- **$Points**: Lihat total poin dan level badge kamu
- **$Leaderboard**: Ranking top 5 pengguna dengan poin tertinggi
- **$Levelbadge**: Lihat daftar badge dari level 1-100
- **$Add_Action <aksi>**: Usulkan aksi hijau baru
- **$Event** (Admin): Mulai event eksklusif dengan aksi spesifik
- **$Claim <cerita>**: Klaim event eksklusif (hanya 1 orang pertama) + 25 poin
- **$Reset_Tips** (Admin): Reset jatah poin harian pengguna
- **$Kategori**: Lihat kategori sampah (organik/anorganik/berbahaya)
- **$Pilah <sampah>**: Cek kategori jenis sampah
- **$Tambah_Kategori**: Tambah jenis sampah baru ke kategori

### 🕸️ Fitur Web Scraping
Mengambil data dari internet untuk memberikan rekomendasi dan informasi:

- **$Quotes**: Ambil quote inspiratif acak dari website
- **$Books**: Rekomendasi buku random dengan cooldown 30 menit (+ 2 poin)
- **$BookDescription**: Buku acak dari database lokal dengan sinopsis lengkap
- **$FindBooks <keyword>**: Cari buku berdasarkan judul atau deskripsi
- **$BooksAdmin** (Admin): Mode diagnostik untuk cek status koneksi scraping
- **$TrueAdminBookDescription <jumlah>** (Owner): Scrape & simpan buku ke database JSON

### 🎮 Fitur Hiburan Umum
Perintah tambahan untuk interaksi santai:

- **$Halo**: Sapaan dari bot
- **$Goodbye**: Emoji senyuman
- **$Emoji**: Emoji random
- **$Dadu**: Roll dadu 1-6 dengan respons unik
- **$Koin**: Lempar koin (Kepala/Ekor)
- **$Passgen <jumlah>**: Generate password acak (4-64 karakter)
- **$Menambahkan <angka1> <angka2>**: Kalkulator penjumlahan
- **$Ulang <jumlah> <kata>**: Ulangi kata N kali
- **$Bebek**: Gambar bebek random
- **$Rubah**: Gambar rubah random

### 🌐 Fitur Website Dashboard
Dashboard interaktif untuk memantau data bot:

- **Home**: Statistik total users, poin hijau, koleksi buku
- **Leaderboard**: Ranking poin hijau users
- **Books**: Lihat koleksi buku dari database
- **Search Books**: Cari buku berdasarkan keyword

---

## 📊 Sistem Level & Badge

Bot menggunakan sistem level berbasis poin hijau:

| Level | Badge | Poin |
|-------|-------|------|
| 1 | 🌱 Newbie | 0-4 |
| 5 | 🍃 Fresh Starter | 20-24 |
| 10 | 🌿 Green Explorer | 45-49 |
| 30 | 🌲 Eco Enthusiast | 145-149 |
| 50 | 🌍 Environmental Hero | 245-249 |
| 100 | 🏆 Legendary Green Champion | 495+ |

---

## 🚀 Cara Setup & Menjalankan

### Prerequisites
- Python 3.12+
- pip (Python package manager)
- Discord bot token
- Git (opsional, untuk push ke GitHub)

### 1. Install Dependencies

```powershell
# Install library Python
pip install discord.py requests beautifulsoup4 certifi flask

# Atau dari requirements.txt
pip install -r requirements.txt
