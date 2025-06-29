# Codec & Steganography System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Aplikasi berbasis web untuk mengompresi, mendekompresi file **gambar**, **audio**, dan **video**, serta menyisipkan dan mengekstrak pesan rahasia pada gambar menggunakan **steganografi LSB (Least Significant Bit)**. Dibangun dengan **Flask** untuk backend dan antarmuka modern menggunakan **HTML**, **CSS**, dan **JavaScript** untuk frontend.

## Deskripsi

Sistem Codec & Steganography memungkinkan pengguna untuk memproses file media dan menyembunyikan pesan dalam gambar dengan antarmuka web yang responsif, modern, dan interaktif. Fitur utama meliputi kompresi/dekompresi dengan tingkat kompresi yang dapat disesuaikan, steganografi LSB untuk gambar, pratinjau input dan output yang lebih kecil, serta sorotan visual untuk pesan yang diekstrak. Desain menggunakan gradien biru-ungu, animasi halus, gaya neumorphism pada form input, dan bilah progres untuk pengalaman pengguna yang optimal.

## Fitur

- **Jenis Media yang Didukung**:
  - **Gambar**: Kompresi ke JPEG, dekompresi ke PNG, embedding/ekstraksi pesan menggunakan LSB.
  - **Audio**: Kompresi ke MP3, dekompresi ke WAV.
  - **Video**: Kompresi ke MP4 (H.264), dekompresi ke MP4 kualitas tinggi.
- **Tingkat Kompresi** (khusus untuk kompresi):
  - **Sangat Kecil**: Ukuran file terkecil, kualitas rendah.
  - **Sedang**: Keseimbangan antara ukuran dan kualitas (default).
  - **Kecil**: Kualitas tinggi, ukuran file lebih besar.
- **Steganografi LSB** (khusus untuk gambar):
  - **Embed Message**: Menyisipkan pesan rahasia ke dalam bit LSB dari piksel RGB.
  - **Extract Message**: Mengekstrak pesan dengan sorotan visual pada hasil.
  - Validasi kapasitas gambar untuk memastikan pesan dapat disisipkan.
- **Antarmuka Pengguna**:
  - Desain modern dengan gradien biru-ungu dan gaya neumorphism pada dropdown/input.
  - Animasi halus (fade-in, slide-in, hover, shake untuk error, rotasi panah dropdown).
  - Pratinjau input dan output yang lebih kecil (maksimum 200px, 150px pada layar kecil).
  - Sorotan visual (gradien dan animasi) untuk pesan yang diekstrak.
  - Bilah progres responsif selama pemrosesan.
  - Responsif untuk desktop dan perangkat mobile.
- **Fungsionalitas**:
  - Pratinjau input (gambar, audio, video) sebelum diproses.
  - Pratinjau output untuk gambar setelah kompresi, dekompresi, atau embedding.
  - Validasi panjang pesan untuk steganografi di frontend dan backend.
  - Penanganan error dengan pesan visual yang jelas.
  - Validasi jenis file dan sanitasi nama file untuk keamanan.

## Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (font Poppins), JavaScript
- **Pustaka Python**:
  - Pillow: Pemrosesan gambar.
  - NumPy: Operasi array untuk steganografi LSB.
  - pydub: Pemrosesan audio.
  - moviepy: Pemrosesan video.
- **Dependensi Eksternal**: FFmpeg (untuk audio dan video)
- **Styling**: CSS kustom dengan gradien, neumorphism, bayangan kotak, dan animasi

## Struktur Proyek

```plaintext
codec_steganography/
├── app.py               # Backend Flask dengan steganografi LSB
├── static/
│   ├── css/
│   │   └── style.css   # Gaya frontend dengan neumorphism dan pratinjau kecil
│   └── js/
│       └── script.js   # Logika frontend untuk pratinjau dan validasi
├── templates/
│   └── index.html      # Halaman HTML utama dengan form input modern
├── output/             # Folder untuk file hasil
└── README.md           # Dokumentasi proyek
```

## Prasyarat

- Python 3.8 atau lebih tinggi
- FFmpeg terinstal dan ditambahkan ke PATH sistem
- Koneksi internet untuk mengunduh dependensi

## Instalasi

1. **Klon Repositori** (ganti dengan URL repositori Anda jika tersedia):

   ```bash
   git clone https://github.com/mohammadraflisumaryono/Codec-System-Website---Sistem-MultiMedia.git
   cd Codec-System-Website---Sistem-MultiMedia
   ```

2. **Buat dan Aktifkan Virtual Environment** (opsional, tetapi disarankan):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instal Dependensi Python**:

   ```bash
   pip install flask Pillow numpy pydub moviepy
   ```

4. **Instal FFmpeg**:

   - Unduh dari [ffmpeg.org](https://ffmpeg.org).
   - Tambahkan ke PATH sistem.
   - Verifikasi instalasi:
     ```bash
     ffmpeg -version
     ```

5. **Siapkan Struktur Proyek**:
   - Pastikan `app.py`, `index.html`, `style.css`, dan `script.js` ditempatkan sesuai struktur di atas.
   - Folder `output` akan dibuat otomatis oleh aplikasi.

## Menjalankan Aplikasi

1. **Jalankan Server Flask**:

   ```bash
   python app.py
   ```

   - Aplikasi akan berjalan di `http://127.0.0.1:5000`.

2. **Akses Antarmuka Web**:
   - Buka browser dan kunjungi `http://127.0.0.1:5000`.

## Cara Penggunaan

1. **Pilih Jenis Media**:
   - Pilih **Gambar** (JPEG/PNG), **Audio** (MP3/WAV/M4A/FLAC), atau **Video** (MP4/MOV/AVI/MKV) dari dropdown modern.
2. **Pilih Aksi**:
   - **Kompresi**: Mengurangi ukuran file dengan tingkat kompresi.
   - **Dekompresi**: Mengembalikan file ke format lossless atau kualitas tinggi.
   - **Embed Message** (khusus gambar): Menyisipkan pesan rahasia menggunakan LSB.
   - **Extract Message** (khusus gambar): Mengekstrak pesan rahasia dengan sorotan visual.
3. **Pilih Tingkat Kompresi** (hanya untuk kompresi):
   - **Sangat Kecil**: Ukuran terkecil, kualitas rendah.
   - **Sedang**: Keseimbangan ukuran dan kualitas (default).
   - **Kecil**: Kualitas tinggi, ukuran lebih besar.
4. **Masukkan Pesan** (untuk Embed Message):
   - Ketik pesan rahasia di input teks (maksimum kapasitas divalidasi berdasarkan ukuran gambar).
5. **Unggah File**:
   - Klik **Choose File** untuk mengunggah file dalam format yang didukung.
   - Pratinjau input (maksimum 200px) akan ditampilkan setelah file dipilih.
6. **Proses File**:
   - Klik **Process** untuk memulai pemrosesan.
   - Bilah progres akan muncul selama pemrosesan.
7. **Hasil**:
   - Untuk **kompresi**, **dekompresi**, atau **embed**: Pratinjau output (maksimum 200px) dan tautan unduhan akan muncul.
   - Untuk **extract**: Pesan yang diekstrak akan ditampilkan dengan sorotan gradien.

## Detail Kompresi dan Steganografi

| Media  | Aksi       | Tingkat Kompresi | Parameter                      | Format Output |
| ------ | ---------- | ---------------- | ------------------------------ | ------------- |
| Gambar | Kompresi   | Sangat Kecil     | Kualitas JPEG 10               | JPEG          |
|        |            | Sedang           | Kualitas JPEG 50               | JPEG          |
|        |            | Kecil            | Kualitas JPEG 80               | JPEG          |
|        | Dekompresi | -                | Lossless                       | PNG           |
|        | Embed      | -                | LSB (1 bit/piksel RGB)         | PNG           |
|        | Extract    | -                | Membaca LSB                    | Teks          |
| Audio  | Kompresi   | Sangat Kecil     | Bitrate MP3 64k                | MP3           |
|        |            | Sedang           | Bitrate MP3 128k               | MP3           |
|        |            | Kecil            | Bitrate MP3 256k               | MP3           |
|        | Dekompresi | -                | Lossless                       | WAV           |
| Video  | Kompresi   | Sangat Kecil     | H.264 CRF 35                   | MP4           |
|        |            | Sedang           | H.264 CRF 28                   | MP4           |
|        |            | Kecil            | H.264 CRF 18                   | MP4           |
|        | Dekompresi | -                | H.264 CRF 18 (kualitas tinggi) | MP4           |

## Catatan

- **Steganografi LSB**:
  - Gunakan gambar beresolusi tinggi (minimal 512x512 piksel) untuk pesan pendek agar kapasitas cukup.
  - Simpan gambar hasil embedding sebagai PNG untuk mencegah kehilangan data.
  - Jangan kompres ulang gambar hasil embedding sebelum ekstraksi.
  - Kapasitas maksimum pesan: `(lebar * tinggi * 3) / 8 - 3` karakter.
- **Pratinjau**:
  - Pratinjau input dan output dibatasi hingga 200px (150px pada layar kecil) untuk efisiensi.
  - Jika pratinjau output gagal, periksa konsol browser (F12) untuk error seperti CORS atau file tidak ditemukan.
- **Performa**:
  - Pemrosesan video besar mungkin lambat. Gunakan server dengan CPU/GPU yang memadai untuk produksi.
- **Keamanan**:
  - Jenis file divalidasi, dan nama file disanitasi untuk mencegah masalah keamanan.
- **Peningkatan Potensial**:
  - Dukungan drag-and-drop untuk unggah file.
  - Progres pemrosesan real-time menggunakan WebSocket.
  - Validasi ukuran file atau pratinjau ukuran sebelum pemrosesan.
  - Tambahan format file yang didukung.

## Tangkapan Layar

_(Tambahkan tangkapan layar antarmuka di sini jika diunggah ke repositori. Contoh:)_

- Antarmuka utama: `screenshots/main-interface.png`
- Proses steganografi: `screenshots/steganography-embed.png`
- Hasil ekstraksi pesan: `screenshots/extract-message.png`
- Pratinjau input/output: `screenshots/preview.png`

## Kontribusi

1. Fork repositori ini.
2. Buat branch untuk fitur baru:
   ```bash
   git checkout -b nama-fitur
   ```
3. Commit perubahan:
   ```bash
   git commit -m "Menambahkan fitur"
   ```
4. Push ke branch:
   ```bash
   git push origin nama-fitur
   ```
5. Buka pull request di repositori.


## Kontak

Untuk pertanyaan, masalah, atau saran, silakan buka isu di repositori atau hubungi pengelola proyek.

---

### Penjelasan Perubahan
1. **Judul dan Deskripsi**:
   - Diperbarui menjadi "Codec & Steganography System" untuk mencerminkan fitur steganografi LSB.
   - Menyebutkan antarmuka modern dengan neumorphism, pratinjau kecil, dan sorotan pesan yang diekstrak.

2. **Fitur**:
   - Menambahkan detail tentang steganografi LSB (embedding dan ekstraksi).
   - Menyebutkan pratinjau input/output yang lebih kecil (200px) dan sorotan visual untuk pesan yang diekstrak.
   - Menyoroti desain dropdown/input dengan gaya neumorphism dan animasi.

3. **Struktur Proyek**:
   - Diperbarui untuk mencerminkan struktur folder yang sama dengan kode terbaru.

4. **Cara Penggunaan**:
   - Menambahkan langkah untuk steganografi (embed dan extract).
   - Menyebutkan pratinjau input/output dan sorotan pesan yang diekstrak.
   - Memperjelas validasi kapasitas pesan untuk embedding.

5. **Detail Kompresi dan Steganografi**:
   - Menambahkan baris untuk `Embed` dan `Extract` pada tabel, dengan detail parameter LSB.
   - Mempertahankan detail kompresi/dekompresi dari versi sebelumnya.

6. **Catatan**:
   - Menambahkan panduan untuk steganografi, termasuk pentingnya menggunakan PNG dan menghindari kompresi ulang.
   - Menyebutkan langkah debugging untuk masalah pratinjau output.

### Catatan Tambahan
- **Pratinjau Output**: Jika masih ada masalah dengan pratinjau output, pastikan folder `output` memiliki izin tulis dan file tersimpan dengan benar. Periksa konsol browser (F12) untuk error seperti "Failed to load preview".
- **Ukuran Gambar untuk Steganografi**: Gunakan gambar minimal 512x512 piksel untuk pesan pendek (misalnya, "Test123"). Kapasitas dihitung di frontend dan backend untuk mencegah error.
- **Debugging**: Jalankan aplikasi dengan `debug=True` untuk log server. Jika pesan tidak terekstrak, pastikan gambar yang diunggah adalah PNG hasil embedding.

Jika Anda ingin menambahkan tangkapan layar atau detail lain ke `README.md`, beri tahu saya! Silakan uji aplikasi dan laporkan jika ada masalah atau penyesuaian lebih lanjut yang diperlukan.