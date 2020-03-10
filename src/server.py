from flask import *
import codecs
import os
import sys,subprocess
import requests
import http.client , urllib
import io
import binascii
import cv2
import threading
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import (Text, Time)
from sqlalchemy import func
import avatarFER as af
import tensorflow as tf

app = Flask(__name__)
detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
gender_model_path = '../trained_models/gender_models/simple_CNN.81-0.96.hdf5'
graph = tf.get_default_graph()
engine = create_engine('sqlite:///emotion.db')  # user.db というデータベースを使うという宣言です
Base = declarative_base()  # データベースのテーブルの親です

class EmoT(Base):  # PythonではUserというクラスのインスタンスとしてデータを扱います
    __tablename__ = 'emotions'  # テーブル名は users です
    id = Column(Integer, primary_key=True, unique=True)  # 整数型のid をprimary_key として、被らないようにします
    emotion = Column(String)  # 文字列の emailというデータを作ります
    Created_At = Column(Time, default=datetime.datetime.now().time())  # 文字列の nameというデータを使います

    # def __repr__(self):
    #     return "User<{}, {}, {}>".format(self.id, self.email, self.name)
Base.metadata.create_all(engine)  # 実際にデータベースを構築します
SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
session = SessionMaker()  # 経路を実際に作成しました

t = session.query(func.count(EmoT.id)).first()
t = str(t)
t = t[1:-2]
print('t:' + t)
ss = session.query(EmoT.emotion).filter(EmoT.id == t).all()
ss = str(ss)
ss = ss[3:-4]
print(ss)

tmp = ""
sendDataToUnity = ""

@app.route('/')
def hello():
    hello = "Hello world"
    return img

@app.route('/hello', methods=['POST' , 'GET']) #Methodを明示する必要あり
def hello2():
    name = "no"
    test = "test"
    if request.method == 'POST':
        print(request.get_json())
        a = request.get_json()
        print(a['emo'])
        a = a['emo']
        # g.sendDataToUnity = a['emo']
        # print('senddata : ' + sendDataToUnity + ' g : ' + g.sendDataToUnity)
        # setData(g.sendDataToUnity)
        SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
        session = SessionMaker()  # 経路を実際に作成しました
        emotmp2 = EmoT(emotion = a)
        session.add(emotmp2)  # user1 をデータベースに入力するための準備をします
        session.commit()  # 実際にデータベースにデータを入れます
        #session.rollback()
        #if()session.query(EmoT).delete()
        cnt = session.query(func.count(EmoT.id)).first()
        cnt = str(cnt)
        cnt = cnt[1:-2]
        print(cnt)
        ss = session.query(EmoT.emotion).filter(EmoT.id == cnt).all()
        ss = str(ss)
        ss = ss[3:-4]
        print('sssssss:' + str(ss) + ' cnt : ' + cnt)
        return a
        #return img
    elif request.method == 'GET' :
        SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
        session = SessionMaker()  # 経路を実際に作成しました
        t = session.query(func.count(EmoT.id)).first()
        t = str(t)
        t = t[1:-2]
        print('get t:' + t)
        ss = session.query(EmoT.emotion).filter(EmoT.id == t).all()
        ss = str(ss)
        ss = ss[3:-4]
        print('get ss' + str(ss))
        return ss
    else:
        #name = "no name."
        return name
    return name

@app.route('/AvatarFER', methods=['POST' , 'GET']) #Methodを明示する必要あり
def FER():
    global graph
    tmp = 'err'
    with graph.as_default():
        if request.method == 'POST':
            filepath = request.get_data()
            filepath = filepath.decode('utf-8')
            print('------------------------------------------------------')
            print(filepath)
            filepath = filepath[:-2]
            print(filepath)
            filepath = '../../../Picture/SS.jpg'
            emo = FER2(filepath)
            return emo
import sys

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input
import tensorflow as tf

def FER2(path) :
    # parameters for loading data and images
    image_path = path
    emotion_labels = get_labels('fer2013')
    gender_labels = get_labels('imdb')
    font = cv2.FONT_HERSHEY_SIMPLEX

    # hyper-parameters for bounding boxes shape
    gender_offsets = (30, 60)
    gender_offsets = (10, 10)
    emotion_offsets = (20, 40)
    emotion_offsets = (0, 0)

    # loading models
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    gender_classifier = load_model(gender_model_path, compile=False)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    gender_target_size = gender_classifier.input_shape[1:3]

    # loading images
    rgb_image = load_image(image_path, grayscale=False)
    gray_image = load_image(image_path, grayscale=True)
    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')

    faces = detect_faces(face_detection, gray_image)
    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
        rgb_face = rgb_image[y1:y2, x1:x2]

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]

        try:
            rgb_face = cv2.resize(rgb_face, (gender_target_size))
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        rgb_face = preprocess_input(rgb_face, False)
        rgb_face = np.expand_dims(rgb_face, 0)
        gender_prediction = gender_classifier.predict(rgb_face)
        gender_label_arg = np.argmax(gender_prediction)
        gender_text = gender_labels[gender_label_arg]

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
        emotion_text = emotion_labels[emotion_label_arg]

        if gender_text == gender_labels[0]:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

        #emo = emotion_text

        print(emotion_text)
        return emotion_text
    else:
        tmp = 'err'
        return tmp
    tmp = 'err'
    return tmp


## おまじない
if __name__ == "__main__":
    app.run(debug=True)
    