# -*- coding: utf-8 -*-
"""
build.py — PyInstaller Derleme Otomasyonu (Muallimun.Net v40.0)
Çalıştırma: python build.py
"""

import os
import sys
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("🚀 ARAPÇA TELAFFUZ VE KONUŞMA ASİSTANI — PYINSTALLER DERLEME")
print("=" * 60)

# PyInstaller kurulu değilse yükle
try:
    import PyInstaller
except ImportError:
    print("📦 PyInstaller yükleniyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

dist_dir = os.path.join(BASE_DIR, "dist")
build_dir = os.path.join(BASE_DIR, "build")
ico_file = os.path.join(BASE_DIR, "ui", "app_icon.ico")

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--name=ArapcaAsistani",
    "--windowed",              # Konsol penceresini gizle
    "--noconfirm",
    "--clean",
    f"--icon={ico_file}" if os.path.exists(ico_file) else "",
    "--add-data=data;data",
    "--add-data=assets;assets",
    "--add-data=ui;ui",
    "--add-data=version.json;.",
    "--collect-all=faster_whisper",
    "--collect-all=sounddevice",
    "--collect-all=pygame",
    "--collect-all=edge_tts",
    "app.py"
]

# Boş argümanları temizle
cmd = [arg for arg in cmd if arg]

print(f"⚙️ Derleme başlatılıyor...")
subprocess.check_call(cmd)

print("\n" + "=" * 60)
print("✅ DERLEME BAŞARIYLA TAMAMLANDI!")
print(f"📁 Çıktı Klasörü: {os.path.join(dist_dir, 'ArapcaAsistani')}")
print("=" * 60)