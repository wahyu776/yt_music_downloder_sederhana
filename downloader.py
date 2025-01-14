import os
import subprocess
import sys
import pyfiglet
from colorama import Fore, init

# Inisialisasi colorama
init(autoreset=True)

# Direktori tempat file MP3 atau video akan disimpan
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")

# Membuat direktori downloads jika belum ada
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Menampilkan header dengan pyfiglet berwarna merah
def print_header():
    ascii_banner = pyfiglet.figlet_format("Downloader", font="slant")
    print(Fore.RED + ascii_banner)

def download_audio(url, audio_format, audio_quality):
    try:
        # Perintah yt-dlp untuk mendownload audio dengan format pilihan
        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", audio_format,
            "--audio-quality", audio_quality,
            "--output", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            url
        ]

        # Menjalankan perintah
        print(f"Sedang mendownload audio dalam format {audio_format.upper()} dengan kualitas {audio_quality}...")
        subprocess.run(command, check=True)
        print(f"Lagu berhasil didownload ke direktori: {DOWNLOAD_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat mendownload: {e}")
    except FileNotFoundError:
        print("yt-dlp tidak ditemukan. Pastikan sudah terinstal di sistem Anda.")

def download_video(url, video_quality):
    try:
        # Menjalankan yt-dlp untuk menampilkan daftar format video yang tersedia
        print("Memuat daftar format video yang tersedia...")
        subprocess.run(["yt-dlp", "--list-formats", url], check=True)
        
        # Perintah yt-dlp untuk mendownload video dengan kualitas yang diminta
        command = [
            "yt-dlp",
            "-f", video_quality,
            "--output", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            url
        ]

        # Menjalankan perintah
        print(f"Sedang mendownload video dengan kualitas {video_quality}...")
        subprocess.run(command, check=True)
        print(f"Video berhasil didownload ke direktori: {DOWNLOAD_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat mendownload: {e}")
        # Memberikan opsi untuk melanjutkan dengan 'bestvideo+bestaudio'
        continue_download = input("Format yang diminta tidak tersedia. Ingin mendownload menggunakan 'bestvideo+bestaudio'? (y/n): ").lower()
        if continue_download == 'y':
            print("Mencoba mendownload menggunakan 'bestvideo+bestaudio'...")
            command_fallback = [
                "yt-dlp",
                "-f", "bestvideo+bestaudio",  # Mendownload video dan audio terbaik terpisah
                "--output", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
                url
            ]
            subprocess.run(command_fallback, check=True)
            print(f"Video dan audio berhasil didownload ke direktori: {DOWNLOAD_DIR}")
        else:
            print("Download dibatalkan.")
    except FileNotFoundError:
        print("yt-dlp tidak ditemukan. Pastikan sudah terinstal di sistem Anda.")

def choose_format():
    while True:
        audio_format = input("Pilih format audio (mp3/m4a/webm) atau ketik 'kembali' untuk kembali: ").lower()
        if audio_format == 'kembali':
            return None
        if audio_format in ['mp3', 'm4a', 'webm']:
            return audio_format
        else:
            print("Format tidak valid. Pilih antara 'mp3', 'm4a', atau 'webm'.")

def choose_audio_quality():
    while True:
        audio_quality = input("Pilih kualitas audio (0=terbaik, 9=terburuk) atau ketik 'kembali' untuk kembali: ").lower()
        if audio_quality == 'kembali':
            return None
        if audio_quality.isdigit() and 0 <= int(audio_quality) <= 9:
            return audio_quality
        else:
            print("Kualitas tidak valid. Pilih antara 0 (terbaik) hingga 9 (terburuk).")

def choose_video_quality():
    while True:
        video_quality = input("Pilih kualitas video (720p, 480p, best, 1080p, dsb) atau ketik 'kembali' untuk kembali: ").lower()
        if video_quality == 'kembali':
            return None
        # Anda bisa menambahkan pengecekan format yang lebih rinci sesuai dengan pilihan kualitas yang lebih spesifik
        valid_qualities = ['480p', '720p', '1080p', 'best', 'worst']
        if video_quality in valid_qualities:
            return video_quality
        else:
            print("Kualitas tidak valid. Pilih antara '480p', '720p', '1080p', 'best', 'worst', dsb.")

def main_menu():
    print_header()
    while True:
        print("\nMenu Utama:")
        print("1. Download Audio")
        print("2. Download Video")
        print("3. Keluar")
        
        choice = input("Pilih opsi (1/2/3): ")
        
        if choice == '1':
            # Menu untuk download audio
            while True:
                url = input("Masukkan URL untuk download audio (ketik 'kembali' untuk kembali): ")
                if url.lower() == 'kembali':
                    break
                if url:
                    audio_format = choose_format()
                    if audio_format:
                        audio_quality = choose_audio_quality()
                        if audio_quality:
                            download_audio(url, audio_format, audio_quality)
                        else:
                            continue
                    else:
                        continue
        elif choice == '2':
            # Menu untuk download video
            while True:
                url = input("Masukkan URL untuk download video (ketik 'kembali' untuk kembali): ")
                if url.lower() == 'kembali':
                    break
                if url:
                    video_quality = choose_video_quality()
                    if video_quality:
                        download_video(url, video_quality)
                    else:
                        continue
        elif choice == '3':
            print("Terima kasih telah menggunakan aplikasi ini!")
            sys.exit()
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main_menu()
