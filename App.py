from flask import Flask, send_file
from PIL import Image
from io import BytesIO
from xkcd_python import Client
import requests

client = Client()
app = Flask(__name__)

def serve_image(img):
    io_img = BytesIO()
    img.save(io_img, 'png')
    io_img.seek(0)
    return send_file(io_img, mimetype='image/png')

@app.after_request
def set_response_headers(response):
    """Sets Cache-Control header to no-cache so GitHub
    fetches new image everytime
    """
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/", methods=['GET'])
def index():
    img_url = client.random()["img"]
    res = requests.get(img_url, stream=True)
    res.raw.decode_content = True
    img = Image.open(res.raw)
    return serve_image(img)