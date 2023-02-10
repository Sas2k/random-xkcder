from flask import Flask, send_file
from PIL import Image
from io import BytesIO
from xkcd import xkcd
import requests

client = xkcd()
app = Flask(__name__)

def serve_image(img, img_id):
    io_img = BytesIO()
    img.save(io_img, 'png')
    io_img.seek(0)
    return send_file(io_img, mimetype='image/png', download_name=f'xkcd-{img_id}.png')

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
    img_id = client.random()["num"]
    res = requests.get(img_url, stream=True)
    res.raw.decode_content = True
    img = Image.open(res.raw)
    return serve_image(img, img_id)

# uncomment this out when running locally
# app.run()