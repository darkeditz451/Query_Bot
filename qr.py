import qrcode

url = "http://192.168.0.107:5000"

img = qrcode.make(url)
img.save("querybot_qr.png")