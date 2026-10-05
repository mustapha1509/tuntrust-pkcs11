#!/bin/bash

echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing requirements..."
pip install -r requirements.txt

echo "[*] Installing PyInstaller..."
pip install pyinstaller

echo "[*] Building executable with PyInstaller..."
pyinstaller --onefile app.py

echo "[✔] Build complete."
echo "[✔] Your executable is in the dist/ folder as app"

echo "[*] To run in production:"
echo "cd dist"
echo "./app"
