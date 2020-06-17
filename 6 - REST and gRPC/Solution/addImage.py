import jsonpickle
import numpy as np
from PIL import Image
import io

def image(data):
    try:
        ioBuffer = io.BytesIO(data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}
    return response


def add(X, Y):
    return X+Y

