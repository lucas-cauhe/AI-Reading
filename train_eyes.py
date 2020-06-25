import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

train_url = './data/train'
test_url = './data/test'

# Take the data from the dataset and tweak it. 

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
            train_url,
            target_size=(28, 28),
            color_mode='grayscale',
            batch_size=64,
            class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
            test_url,
            target_size=(28, 28),
            color_mode='grayscale',
            batch_size=64,
            class_mode='categorical')

batch_size = 64
input_shape = (28, 28, 1)

# Training model

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(
    train_generator,
    steps_per_epoch=2000,
    epochs=15,
    validation_data=validation_generator,
    validation_steps=1000)
print('Model succesfully trained')

#You can also evaluate the model and then save it.

model.save('weights.h5')
print('weights correctly saved')