import io
from flask import Flask, jsonify, request
import base64
from PIL import Image
import cv2
import numpy as np


from aiModels.bicepCurl import recieve_frame

api = Flask(__name__)


@api.route('/bicepCurl', methods=['POST'])
def process():

    encoded_data = request.json
    
    decodedData = base64.b64decode(encoded_data)

    decodedImage = base64.decodebytes(decodedData)

    image = Image.open(io.BytesIO(decodedImage))

    img = np.asarray(image)

    #x to show returned image
    x = recieve_frame(img)

    cv2.imwrite('try4.png', x)

    #TODO: return needed response
    return jsonify({'msg': 'success'})

if __name__ == '__main__':
    api.run(port=5000, debug=True)
