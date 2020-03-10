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

app = Flask(__name__)

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
    tmp = 'err'
    if request.method == 'POST':
        filepath = request.get_data()
        filepath = filepath.decode('utf-8')
        print('------------------------------------------------------')
        print(filepath)
        filepath = filepath[:-2]
        print(filepath)
        filepath = '../../Assets/Picture/SS.jpg'
        emo = af.FER(filepath)
        print(emo)
        return emo
    else:
        return tmp
    return tmp


## おまじない
if __name__ == "__main__":
    app.run(debug=True)
    