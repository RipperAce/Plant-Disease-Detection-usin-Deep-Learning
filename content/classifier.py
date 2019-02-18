import os

from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint


#create classifier 
classifier = Sequential()

#adding convolution layer
classifier.add(Convolution2D(32, 3, 3, input_shape = (256, 256, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2), strides = (2,2)))
classifier.add(Convolution2D(32, 3, 3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2), strides = (2,2)))
classifier.add(Flatten())
classifier.add(Dense(output_dim = 128, activation = 'relu'))
classifier.add(Dense(output_dim = 4, activation = 'softmax'))

#compiling
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

#making Image size same
from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        'D:/advait data/dataset/train',
        target_size=(256, 256),
        batch_size=32,
        class_mode='categorical')

test_set = test_datagen.flow_from_directory(
        'D:/advait data/dataset/test',
        target_size=(256, 256),
        batch_size=32,
        class_mode='categorical')
print('TRAINING:',training_set)
print('TEST: ',test_set)


#checking if already a weight file exists. if it does loads it into the model
if os.path.isfile("modelCNN.h5") :
		classifier.load_weights("modelCNN.h5")

#checkpoint saves the model.
filepath="modelCNN.h5"		
checkpoint1 = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
	

classifier.summary()
classifier.fit_generator(
        training_set,
        steps_per_epoch=1954,
        epochs=10,
        validation_data=test_set,
        validation_steps=505,callbacks=[checkpoint1,])


disease = ['Apple Scab','Black rot','Cedar rust','healthy']

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
#from keras.applications.vgg16 import preprocess_input
#from keras.applications.vgg16 import decode_predictions
# load the model
#model = VGG16()
# load an image from file
image = load_img('C:/Users/Bhushan/Desktop/mlearning/src/plant disease/data.jpg', target_size=(256, 256))
# convert the image pixels to a numpy array
image = img_to_array(image)
# reshape data for the model
image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

yhat = classifier.predict(image)
print(yhat)

import numpy as np
print(disease[np.argmax(yhat)])

#save as json file
from keras.models import model_from_json

model_json = classifier.to_json()
with open("modelCNN.json", "w") as json_file:
    json_file.write(model_json)
# # serialize weights to HDF5
# classifier.save_weights("modelCNN.h5")

# print("Saved model to disk")