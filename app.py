from flask import Flask, jsonify, request
from pkcs11_utils import list_certs, sign_message
import base64
from waitress import serve

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "version": "1.0",
        "description": "PKCS#11 API for certificate management and signing",
        "endpoints": {
            "/certs": "List available certificates",
            "/sign": "Sign a message [{ \"message\": \"your message here\" }]",
            "/sign-xml": "Sign XML data [{ \"signed_info\": \"base64 encoded XML data\" }]"
        }
    })

@app.route("/certs", methods=["GET"])
def get_certs():
    try:
        certs = list_certs()
        return jsonify(certs)
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching certificates"}), 500

@app.route("/sign", methods=["POST"])
def sign():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in JSON body"}), 400

    try:
        message = data["message"].encode()
        signature = sign_message(message)
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        return jsonify({"signature": signature_b64})
    except Exception as e:
        return jsonify({"error": "An error occurred while signing the message"}), 500

@app.route("/sign-xml", methods=["POST"])
def sign_xml():
    data = request.json
    if not data or "signed_info" not in data:
        return jsonify({"error": "Missing 'signed_info' in JSON body"}), 400

    try:
        c14n_bytes = base64.b64decode(data["signed_info"])
        signature = sign_message(c14n_bytes)
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        return jsonify({"signature": signature_b64})
    except Exception as e:
        return jsonify({"error": "An error occurred while signing the XML data"}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8088)