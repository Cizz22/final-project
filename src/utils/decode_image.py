from base64 import decodebytes
from .celery import celery_app


def decodeImage(images):
    for filename, image in images.items():
        decode_image = decodebytes(bytes(image, "utf-8"))
        with open(f"static/{filename}", "wb") as fh:
            fh.write(decode_image)
