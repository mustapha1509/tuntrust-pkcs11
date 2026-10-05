# PKCS#11 Signing API

Small Flask API for working with a PKCS#11-compatible token. It can list
certificates available on the token and sign plain messages or canonicalized XML
data with the first private key found on the token.

## Project Files

- `app.py` - Flask application and HTTP routes.
- `pkcs11_utils.py` - PKCS#11 token access, certificate parsing, and signing.
- `load_config.py` - Loads `config.ini` from the script or executable folder.
- `config.ini` - Local PKCS#11 library path and user PIN configuration.
- `requirements.txt` - Python dependencies.
- `build.sh` - Linux/macOS PyInstaller build helper.
- `build.bat` - Windows PyInstaller build helper.
- `run.bat` - Windows helper to start the built executable in the background.

## Requirements

- Python 3
- A PKCS#11-compatible USB token or smart card
- The vendor PKCS#11 library installed on the machine
- Token user PIN

Python dependencies are listed in `requirements.txt`:

```txt
flask
python-pkcs11
cryptography
waitress
```

## Configuration

Edit `config.ini` before running the API:

```ini
[PKCS11]
LIBRARY_PATH = C:\Windows\System32\tuntrust_pkcs11.dll
USER_PIN = your-token-pin
```

`LIBRARY_PATH` must point to the PKCS#11 library provided by the token vendor.
On Windows this is usually a `.dll`; on Linux it is commonly a `.so`; on macOS
it may be a `.dylib`.

Keep `config.ini` private because it contains the token PIN.

## Development Setup

From this directory:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

The API runs on:

```text
http://localhost:8088
```

On Windows, activate the virtual environment with:

```bat
venv\Scripts\activate.bat
```

## API Endpoints

### Health and Metadata

```http
GET /
```

Returns the API version, description, and available endpoints.

### List Certificates

```http
GET /certs
```

Returns certificates found on the token, including label, subject, issuer,
serial number, validity dates, and the certificate value encoded as Base64.

Example:

```bash
curl http://localhost:8088/certs
```

### Sign a Message

```http
POST /sign
Content-Type: application/json
```

Request body:

```json
{
  "message": "your message here"
}
```

Example:

```bash
curl -X POST http://localhost:8088/sign \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

The response contains a Base64-encoded signature:

```json
{
  "signature": "..."
}
```

### Sign Canonicalized XML Data

```http
POST /sign-xml
Content-Type: application/json
```

Request body:

```json
{
  "signed_info": "base64-encoded-canonicalized-xml"
}
```

Example:

```bash
curl -X POST http://localhost:8088/sign-xml \
  -H "Content-Type: application/json" \
  -d '{"signed_info":"PHhtbD5kYXRhPC94bWw+"}'
```

The API decodes `signed_info`, signs the bytes, and returns the signature as
Base64.

## Build an Executable

### Windows

Run:

```bat
build.bat
```

The executable is created at:

```text
dist\app.exe
```

`build.bat` also includes `config.ini` in the PyInstaller bundle.

### Linux or macOS

Run:

```bash
chmod +x build.sh
./build.sh
```

The executable is created at:

```text
dist/app
```

If the packaged app cannot find `config.ini`, place a copy next to the generated
executable.

## Production Notes

- The service listens on `0.0.0.0:8088` through Waitress.
- Protect the API at the network level; the endpoints can access private keys
  through the configured token.
- Do not commit real PINs, private configuration, or token-specific secrets.
- The current signing mechanism is `SHA256_RSA_PKCS`.
- The first private key returned by the token is used for signing.

## Troubleshooting

- `Token not found`: confirm the USB token or smart card is connected and the
  vendor driver is installed.
- PKCS#11 library loading errors: verify `LIBRARY_PATH` points to the correct
  vendor library for the current operating system and CPU architecture.
- PIN errors: update `USER_PIN` in `config.ini`.
- No private key found: confirm the token contains a usable private key and that
  the configured PIN has access to it.
