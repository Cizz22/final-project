from base64 import decodebytes
from server import celery


@celery.task(name="decode_image")
def decodeImage(images):
    for filename, image in images.items():
        decode_image = decodebytes(bytes(image, "utf-8"))
        with open(f"static/image/{filename}.jpg", "wb") as fh:
            fh.write(decode_image)
