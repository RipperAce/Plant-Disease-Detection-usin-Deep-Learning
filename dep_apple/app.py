from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np


import tensorflow as tf
global graph,model
graph = tf.get_default_graph()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.4
session = tf.Session(config=config)


# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

width,height = 256,256

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/Apple_new.h5'

#Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
# print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(256, 256))
    img = img.resize((width,height))
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
#    x = image.reshape(1,image.shape[0],image.shape[1],image.shape[2])

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
#    x = preprocess_input(x, mode='caffe')
    print(model.predict_proba(x))
    preds = model.predict(x)
    print(preds)
    return preds


@app.route('/apple', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        with graph.as_default():
            preds = model_predict(file_path, model)
        disease = ['Apple Scab','Black rot','Cedar rust','Healthy']
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
#        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
#        result = str(pred_class[0][0][1])               # Convert to string
        print(preds)

        import numpy as np
        result = disease[np.argmax(preds)]
#        num = np.argmax(preds)
#        array=(result,num)
        return result
    return None

if __name__ == '__main__':
     app.run(port=5002, debug=True)

    # Serve the app with gevent
#    http_server = WSGIServer(('', 5000), app)
 #   http_server.serve_forever()
