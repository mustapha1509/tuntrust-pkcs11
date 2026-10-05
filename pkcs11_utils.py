from pkcs11 import lib, Attribute, Mechanism
from load_config import LIBRARY_PATH, USER_PIN
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import base64

pkcs11 = lib(LIBRARY_PATH)

def get_token():
    for slot in pkcs11.get_slots():
        token = slot.get_token()
        return token
    print("No token found")
    raise Exception("Token not found")

def list_certs():
    with get_token().open(user_pin=USER_PIN) as session:
        certs = []
        for cert_obj in session.get_objects({Attribute.CLASS: 0x01}):  # CKO_CERTIFICATE
            label = cert_obj[Attribute.LABEL]
            cert_data = cert_obj[Attribute.VALUE]
            try:
                cert = x509.load_der_x509_certificate(cert_data, backend=default_backend())

                certs.append({
                    "label": label,
                    "subject": cert.subject.rfc4514_string(),
                    "issuer": cert.issuer.rfc4514_string(),
                    "serial_number": hex(cert.serial_number),
                    "not_valid_before": cert.not_valid_before_utc.isoformat(),
                    "not_valid_after": cert.not_valid_after_utc.isoformat(),
                    "certificate_base64": base64.b64encode(cert_data).decode('utf-8')
                })
            except Exception as e:
                print(f"Error parsing certificate {label}: {str(e)}")
                certs.append({
                    "label": label,
                    "error": f"Could not parse certificate: {str(e)}"
                })

        return certs

def sign_message(message: bytes):
    with get_token().open(user_pin=USER_PIN) as session:
        priv_keys = list(session.get_objects({Attribute.CLASS: 0x03}))  # CKO_PRIVATE_KEY
        if not priv_keys:
            print("No private key found")
            raise Exception("No private key found")
        private_key = priv_keys[0]
        signature = private_key.sign(message, mechanism=Mechanism.SHA256_RSA_PKCS)
        return signature
