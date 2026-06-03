import qrcode
import os

def generate_qr(url):
    path = "static/qrcode"
    os.makedirs(path, exist_ok=True)

    img = qrcode.make(url)
    img.save(os.path.join(path, "ngrok_qr.png"))

    print("QR dibuat untuk:", url)


if __name__ == "__main__":
    # WAJIB pakai URL NGROK AKTIF
    url = "https://celtic-freeing-ungodly.ngrok-free.dev"
    generate_qr(url)