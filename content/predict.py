import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

#load trained model
classifier = load_model('modelCNN.h5')



# load an image from file
image = load_img('data.jpg', target_size=(256, 256))

# convert the image pixels to a numpy array
image = img_to_array(image)
# reshape data for the model
image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
yhat = classifier.predict(image)
print(yhat)


disease = ['Apple Scab','Black rot','Cedar rust','healthy']
print(disease[np.argmax(yhat)])

