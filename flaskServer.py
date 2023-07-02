import io
from flask import Flask, jsonify, request
import base64
from PIL import Image
import cv2
import numpy as np

from aiModels.bicepCurl import recieve_frame as bc
from aiModels.squat import recieve_frame as sq
#TODO:name of functions (recieve_frame) should be changed 

api = Flask(__name__)

@api.route('/bicepCurl', methods=['POST'])
def bicupCurl():

    encoded_data = request.json
    
    decodedData = base64.b64decode(encoded_data)

    decoded_image_data = base64.decodebytes(decodedData)

    image = Image.open(io.BytesIO(decoded_image_data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList = bc(img)

    #cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList})     


@api.route('/squat', methods=['POST'])
def squat():

    encoded_data = request.json
    
    decodedData = base64.b64decode(encoded_data)

    decoded_image_data = base64.decodebytes(decodedData)

    image = Image.open(io.BytesIO(decoded_image_data))

    img = np.asarray(image)

    x, counter, feedback = sq(img)

    #cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback})      


if __name__ == '__main__':
    api.run(port=5000, debug=True)
