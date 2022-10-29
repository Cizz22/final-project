import base64
from server import celery

@celery.task(name="decode_image")
def decodeImage(image, filename):
    with open(f"static/images/{filename}", "wb") as fh:
        fh.write(base64.decodebytes(bytes(image, "utf-8")))
