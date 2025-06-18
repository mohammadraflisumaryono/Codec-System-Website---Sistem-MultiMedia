# Sistem Codec

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Aplikasi berbasis web untuk mengompresi dan mendekompresi file **gambar**, **audio**, dan **video** dengan tingkat kompresi yang dapat disesuaikan. Dibangun menggunakan **Flask** untuk backend dan antarmuka modern dengan **HTML**, **CSS**, dan **JavaScript** untuk frontend.

## Deskripsi

Sistem Codec memungkinkan pengguna untuk memproses file media dengan mudah melalui antarmuka web yang responsif dan elegan. Fitur utama meliputi kompresi dan dekompresi untuk tiga jenis media dengan tingkat kompresi yang dapat dipilih (Sangat Kecil, Sedang, Kecil). Desainnya menggunakan gradien dinamis biru-ungu, animasi halus, dan bilah progres untuk pengalaman pengguna yang interaktif.

## Fitur

- **Jenis Media yang Didukung**:
  - **Gambar**: Kompresi ke JPEG, dekompresi ke PNG.
  - **Audio**: Kompresi ke MP3, dekompresi ke WAV.
  - **Video**: Kompresi ke MP4 (H.264), dekompresi ke MP4 kualitas tinggi.
- **Tingkat Kompresi** (khusus untuk kompresi):
  - **Sangat Kecil**: Ukuran file terkecil, kualitas rendah.
  - **Sedang**: Keseimbangan antara ukuran dan kualitas (default).
  - **Kecil**: Kualitas tinggi, ukuran file lebih besar.
- **Antarmuka Pengguna**:
  - Desain bersih dengan gradien biru-ungu.
  - Animasi halus (fade-in, slide-in, efek hover, shake untuk error).
  - Bilah progres responsif selama pemrosesan.
  - Responsif untuk desktop dan perangkat mobile.
- **Fungsionalitas**:
  - Pratinjau file (gambar, audio, video) sebelum diproses.
  - Validasi jenis file dan penanganan nama file yang aman.

## Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (font Poppins), JavaScript
- **Pustaka Python**:
  - Pillow: Pemrosesan gambar.
  - pydub: Pemrosesan audio.
  - moviepy: Pemrosesan video.
- **Dependensi Eksternal**: FFmpeg (untuk audio dan video)
- **Styling**: CSS kustom dengan gradien, bayangan kotak, dan animasi

## Struktur Proyek

```plaintext
codec_app/
├── app.py               # Backend Flask
├── static/
│   ├── css/
│   │   └── style.css   # Gaya frontend
│   └── js/
│       └── script.js   # Logika frontend
├── templates/
│   └── index.html      # Halaman HTML utama
├── output/             # Folder untuk file hasil
└── README.md           # Dokumentasi proyek
```

## Prasyarat

- Python 3.8 atau lebih tinggi
- FFmpeg terinstal dan ditambahkan ke PATH sistem
- Koneksi internet untuk mengunduh dependensi

## Instalasi

1. **Klon Repositori**:

   ```bash
   https://github.com/mohammadraflisumaryono/Codec-System-Website---Sistem-MultiMedia.git
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
   pip install flask Pillow pydub moviepy
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
   - Pilih **Gambar** (JPEG/PNG), **Audio** (MP3/WAV), atau **Video** (MP4) dari dropdown.
2. **Pilih Aksi**:
   - Pilih **Kompresi** atau **Dekompresi**.
3. **Pilih Tingkat Kompresi** (hanya untuk kompresi):
   - **Sangat Kecil**: Ukuran terkecil, kualitas rendah.
   - **Sedang**: Keseimbangan ukuran dan kualitas.
   - **Kecil**: Kualitas tinggi, ukuran lebih besar.
4. **Unggah File**:
   - Klik **Pilih File** untuk mengunggah file (format yang didukung: JPG/PNG untuk gambar, MP3/WAV/M4A/FLAC untuk audio, MP4/MOV/AVI/MKV untuk video).
5. **Proses File**:
   - Klik **Proses** untuk memulai pemrosesan.
   - Bilah progres akan muncul selama pemrosesan.
   - File yang diunggah akan ditampilkan sebagai pratinjau (gambar, audio, atau video).
6. **Unduh Hasil**:
   - Setelah selesai, tautan unduhan akan muncul untuk file terkompresi atau terdekompresi.

## Detail Kompresi

| Media  | Aksi       | Tingkat Kompresi | Parameter                      | Format Output |
| ------ | ---------- | ---------------- | ------------------------------ | ------------- |
| Gambar | Kompresi   | Sangat Kecil     | Kualitas JPEG 10               | JPEG          |
|        |            | Sedang           | Kualitas JPEG 50               | JPEG          |
|        |            | Kecil            | Kualitas JPEG 80               | JPEG          |
|        | Dekompresi | -                | Lossless                       | PNG           |
| Audio  | Kompresi   | Sangat Kecil     | Bitrate MP3 64k                | MP3           |
|        |            | Sedang           | Bitrate MP3 128k               | MP3           |
|        |            | Kecil            | Bitrate MP3 256k               | MP3           |
|        | Dekompresi | -                | Lossless                       | WAV           |
| Video  | Kompresi   | Sangat Kecil     | H.264 CRF 35                   | MP4           |
|        |            | Sedang           | H.264 CRF 28                   | MP4           |
|        |            | Kecil            | H.264 CRF 18                   | MP4           |
|        | Dekompresi | -                | H.264 CRF 18 (kualitas tinggi) | MP4           |

## Catatan

- **Performa**: Pemrosesan video untuk file besar bisa lambat. Gunakan server dengan CPU/GPU yang memadai untuk penggunaan produksi.
- **Ukuran File**: Tingkat "Sangat Kecil" menghasilkan file kecil tetapi kualitas rendah. Pilih "Kecil" untuk kualitas lebih baik.
- **Keamanan**: Jenis file divalidasi, dan nama file disanitasi untuk mencegah masalah keamanan.
- **Peningkatan Potensial**:
  - Dukungan drag-and-drop untuk unggah file.
  - Progres pemrosesan real-time menggunakan WebSocket.
  - Validasi ukuran file atau pratinjau ukuran sebelum pemrosesan.
  - Tambahan format file yang didukung.

## Tangkapan Layar

_(Tambahkan tangkapan layar antarmuka di sini jika diunggah ke repositori. Contoh:)_

- Antarmuka utama: `screenshots/main-interface.png`
- Proses kompresi: `screenshots/compression-progress.png`
- Hasil unduhan: `screenshots/download-result.png`

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

## Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).

## Kontak

Untuk pertanyaan, masalah, atau saran, silakan buka isu di repositori atau hubungi pengelola proyek.
