@echo off
echo [*] Creating virtual environment...
python -m venv venv

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Upgrading pip...
python -m pip install --upgrade pip

echo [*] Installing requirements...
pip install -r requirements.txt

echo [*] Installing PyInstaller...
pip install pyinstaller

echo [*] Building executable with PyInstaller...
#pyinstaller --onefile app.py
pyinstaller --onefile app.py --collect-all pkcs11 --add-data "config.ini;."

echo [✔] Build complete.
echo [✔] Your executable is in the dist\ folder as app.exe

echo [*] To run in production:
echo cd dist
echo app.exe
