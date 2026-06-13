# Analisis Proyek: Surfe Auto Bot

## Deskripsi Lengkap
Surfe Auto Bot adalah aplikasi otomasi berbasis Python yang dirancang untuk melakukan tugas secara otomatis pada platform **surfe.be** melalui ekstensi browser. Aplikasi ini menggunakan teknik **Image Recognition** (pengenalan gambar) untuk berinteraksi dengan elemen UI di layar.

### Komponen Utama:
1.  **`main.py`**: Berisi logika inti otomasi, termasuk kontrol jendela browser, penanganan gambar, deteksi URL, penanganan captcha, dan pelaporan tugas yang bermasalah.
2.  **`gui.py`**: Antarmuka grafis (GUI) berbasis Tkinter yang memungkinkan pengguna untuk memulai, menghentikan, dan melewati (skip) tugas dengan log real-time.
3.  **`config.py`**: File konfigurasi yang menyimpan parameter seperti tingkat kepercayaan gambar (`CONFIDENCE`), batas waktu (`TIMEOUT`), dan aturan aksi berdasarkan URL.
4.  **`images/`**: Folder penyimpanan dataset gambar yang digunakan sebagai referensi untuk klik dan deteksi status (misalnya: tombol start, indikator captcha, error page).
5.  **`script.sh`**: Skrip bash untuk instalasi dependensi sistem (khusus Linux) dan pengaturan lingkungan virtual (`.venv`).

### Alur Kerja:
Aplikasi akan memfokuskan jendela browser, membuka ekstensi Surfe, mencari tugas yang tersedia, dan menjalankannya. Jika menemukan kendala seperti captcha atau halaman error, bot memiliki logika untuk mencoba menyelesaikannya atau melaporkan masalah tersebut agar tugas dilewati.

---

## Daftar Bug & Masalah (Identifikasi)

1.  **Ketergantungan Platform (Linux-only):** 
    *   Fungsi `browser_fokus` menggunakan `xdotool`, yang hanya tersedia di Linux (X11). Aplikasi memang dirancang untuk platform linux
2.  **Modularitas Kode:**
    *   Folder `core/` dan `tasks/` saat ini kosong (hanya berisi `__pycache__`). Seluruh logika menumpuk di `main.py`, membuatnya sulit dipelihara seiring bertambahnya fitur.
3.  **Typo pada Output Log:**
    *   Di `main.py`, fungsi `handle_special_action` memiliki baris: `print(f"DETECTED] {str(action).replace("_", " ")}")`. Kurang kurung buka `[` di awal string.
4.  **Penanganan Tab Ganda:**
    *   Fungsi `handle_visit` memanggil `close_tab()` dan kemudian memanggil `handle_surfe_report` yang di dalamnya juga melakukan penutupan tab atau pembukaan ekstensi. Ada potensi tab tertutup secara tidak sengaja atau referensi jendela hilang.
5.  **Efisiensi Pencarian Gambar:**
    *   Fungsi `find_image` melakukan iterasi secara berurutan pada semua gambar dalam folder. Jika folder berisi banyak gambar, ini akan memperlambat respon bot.
6.  **Konfigurasi Hardcoded:  (BIARKAN SEPERTI APA ADAYA)**
    *   `BROWSER = "Chromium"` di `config.py` bersifat kaku. Jika pengguna menggunakan Chrome, Brave, atau browser lain, mereka harus mengedit file kode secara manual.
7.  **Manajemen State pada GUI:**
    *   `stop_bot` hanya mengubah variabel `running = False`, namun loop di `main.py` mungkin masih tertahan di `time.sleep` atau `wait_for` yang lama, sehingga bot tidak langsung berhenti.
8.  **Error Handling yang Terlalu Luas:**
    *   Blok `try...except Exception: continue` di `find_image` menyembunyikan semua jenis error (termasuk jika file gambar rusak), yang mempersulit debugging.

---

## Saran Improvisasi & Fitur Baru

1.  **Modularisasi (Refactoring):**
    *   Pindahkan fungsi utilitas (gambar, klik, window) ke `core/`.
    *   Pindahkan logika spesifik tugas (surfe, youtube, etc.) ke `tasks/`.
2.  **Sistem Logging yang Lebih Baik:**
    *   Gunakan modul `logging` bawaan Python daripada `print` untuk manajemen level log (INFO, DEBUG, ERROR) dan opsi simpan ke file.
4.  **Peningkatan GUI:**
    *   Tambahkan statistik (Jumlah tugas selesai, jumlah report, waktu berjalan).
5.  **Optimasi Image Recognition:**
    *   Gunakan `region` pada `pyautogui.locateOnScreen` jika posisi elemen sudah diketahui (misalnya posisi ekstensi biasanya di pojok kanan atas).
    *   Gunakan `locateAllOnScreen` atau caching hasil lokasi untuk mempercepat deteksi.
7.  **Pembersihan URL Rules:**
    *   Update `RULES_URL_ACTIONS` di `config.py` dengan data yang valid dan hapus contoh placeholder seperti `example.com`.
8.  **Robustness (Ketahanan):**
    *   Tambahkan fungsi untuk mendeteksi jika browser tertutup secara tiba-tiba dan mencoba membukanya kembali.
    *   Implementasikan mekanisme "Heartbeat" untuk memastikan bot tidak macet (stuck).
