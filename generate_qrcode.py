import qrcode
import os

os.makedirs(
    'static/qrcode',
    exist_ok=True
)

url = "http://192.168.1.89:5001"

img = qrcode.make(url)

img.save(
    "static/qrcode/web_mipa.png"
)

print("QR Code berhasil dibuat")