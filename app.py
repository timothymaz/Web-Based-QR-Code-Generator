from flask import Flask, render_template, send_file, request
import qrcode
from io import BytesIO
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def sanitize_input(data):
    # Allow alphanumeric characters, spaces, and some common symbols
    data = re.sub(
        r'[^a-zA-Z0-9\s\.\,\-\_\:\@\#\$\%\&\*\+\=\(\)\[\]\{\}\<\>\?]', '', data)
    # Limit input length to 1024 characters
    return data[:1024]


@app.route('/generate', methods=['GET'])
def generate_qrcode():
    data = request.args.get('data', '')

    if not data:
        return "No data provided for QR code generation", 400

    # Sanitize the input
    data = sanitize_input(data)

    img = generate_qrcode_image(data)
    img_buffer = BytesIO()
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')


@app.route('/generate_wifi', methods=['GET'])
def generate_wifi_qrcode():
    ssid = request.args.get('ssid', '')
    password = request.args.get('password', '')
    auth_type = request.args.get('auth_type', 'WPA')

    if not ssid:
        return "No SSID provided for Wi-Fi QR code generation", 400

    wifi_data = f"WIFI:T:{auth_type};S:{ssid};P:{password};;"

    img = generate_qrcode_image(wifi_data)
    img_buffer = BytesIO()
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')


def generate_qrcode_image(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


if __name__ == '__main__':
    app.run(debug=True)
