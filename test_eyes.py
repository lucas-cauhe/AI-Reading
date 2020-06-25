from keras.models import load_model
from tkinter import *
import tkinter as tk
import PIL
import win32gui
from PIL import ImageGrab, Image, ImageTk
import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, isdir
import Pmw, sys

# You must first download the Haarcascade files.
face_cascade = cv2.CascadeClassifier(r'C:\Users\cauhe\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(r'C:\Users\cauhe\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\cv2\data\haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

# Taking a picture from the reader's eye and saving it as a .png image

def make_zoom():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            eyes = cv2.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(255,255,255),1)
            clone = eyes.copy()
            img_final = clone[ey:ey+eh,ex:ex+ew]
            img_final = cv2.resize(img_final,None,fx=9, fy=10, interpolation = cv2.INTER_LINEAR)
            img_final = cv2.medianBlur(img_final,5)
            cv2.imshow('img', img_final) # Just if you want to see how your eye looks like
            cv2.imwrite('Eye.png', img_final)
            
model = load_model('weights.h5')
categories = ['s', 's-e', 'n', 'n-e', 'n-w', 'mid', 'e', 'w']

# Take the eye's image and turn it into an array that predict() function can understand

def prepare(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  
    new_array = cv2.resize(img_array, (28, 28))  
    return new_array.reshape(1, 28, 28, 1)

# Display a Label wherever the eye is looking
# Since this is a prototype the entire screen will get yellow 
# so you can change the color to a lighter one

def show_label(cat):
    if cat in categories:
        label = tk.Label(bg='yellow', width=50, height=20)
        if 's' in cat:
            label.place(x=400, y=300, anchor='s')
            
        elif 'n' in cat:
            label.place(x=400, y=0, anchor='n')
            
        else:
            if 'w' in cat:
                label.place(x=0, y=150, anchor='w')
                
            if 'e' in cat:
                label.place(x=800, y=150, anchor='e')
                
            else:
                label.place(x=400, y=150)
            
# Turn the camera on   

width, height = 800, 300
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()

root.bind('<Escape>', lambda e: root.quit())
root.title('Video')
lmain = tk.Label(root)
lmain.pack()

def make_prediction():
    make_zoom()
    prediction = model.predict([prepare('Eye.png')])

    show_pred = np.argmax(prediction, axis=1)
    cat = categorias[show_pred[0]]
    #show_cat = tk.Label(text=cat)
    #show_cat.pack()
    show_label(cat)

# Open whatever file you want to read and run the labeling function

filename = 'hello.txt'
top = Frame(root); top.pack(side='top')
text = Pmw.ScrolledText(top)
text.insert('end', open(filename,'r').read())
text.pack()
def show_text():
    make_prediction()
    lmain.after(2000, show_text)
    
show_text()
root.mainloop()
