import os
import subprocess
import sys

# Direktori tempat file MP3 akan disimpan
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")

# Membuat direktori downloads jika belum ada
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_audio(url):
    try:
        # Perintah yt-dlp untuk mendownload audio
        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--output", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            url
        ]

        # Menjalankan perintah
        print("Sedang mendownload lagu...")
        subprocess.run(command, check=True)
        print(f"Lagu berhasil didownload ke direktori: {DOWNLOAD_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat mendownload: {e}")
    except FileNotFoundError:
        print("yt-dlp tidak ditemukan. Pastikan sudah terinstal di sistem Anda.")

def main():
    print("=== Aplikasi Downloader Lagu ===")
    while True:
        url = input("Masukkan URL (atau ketik 'keluar' untuk keluar): ")
        if url.lower() == 'keluar':
            print("Terima kasih telah menggunakan aplikasi ini!")
            sys.exit()
        if url:
            download_audio(url)
        else:
            print("URL tidak boleh kosong. Silakan coba lagi.")

if __name__ == "__main__":
    main()
