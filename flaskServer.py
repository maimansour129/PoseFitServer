from flask import Flask, jsonify, request
from PIL import Image
import numpy as np
import io
# import cv2

from aiModels.bicepCurl import receive_frame as bc
from aiModels.squat import receive_frame as sq
from aiModels.jumpingJacks import receive_frame as jj
from aiModels.lunges import receive_frame as Lunges
from aiModels.pushups import receive_frame as pu
from aiModels.shoulderPress import receive_frame as sp
from aiModels.tricepsKickBack import receive_frame as tc

api = Flask(__name__)

#bicepCurl Endpoint
@api.route('/63fcc0904e37e48dc9f92e61', methods=['POST'])
def bicupCurl():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = bc(img)

    #cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

#squat Endpoint
@api.route('/649f22512e97b6442159d01f', methods=['POST'])
def squat():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = sq(img)

    # cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

#jumpingJacks Endpoint
@api.route('/63fcc0be4e37e48dc9f92e63', methods=['POST'])
def jumpingJacks():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = jj(img)

    # cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

#Lunges Endpoint
@api.route('/64a5b3d4aa89be083ce2c599', methods=['POST'])
def lunges():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = Lunges(img)

    # cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

#pushUps Endpoint
@api.route('/649f21392e97b6442159d01c', methods=['POST'])
def pushUps():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = pu(img)

    # cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

#shoulderPress Endpoint
@api.route('/649f22b62e97b6442159d020', methods=['POST'])
def shoulderPress():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = sp(img)

    # cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

#tricepsKickBack Endpoint
@api.route('/649f21ec2e97b6442159d01e', methods=['POST'])
def tricepsKickBack():

    image = Image.open(io.BytesIO(request.data))

    img = np.asarray(image)

    x, counter, feedback, landmarksList, poseIsCorrect = tc(img)

    # cv2.imwrite('try4.png', x)

    return jsonify({'reps': counter, 'correction': feedback, 'landmarks': landmarksList, 'poseIsCorrect': poseIsCorrect})

if __name__ == '__main__':
    api.run(port=5000, debug=True,host="0.0.0.0")