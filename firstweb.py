#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' First Web 应用 '

from flask import Flask,render_template ,jsonify,request
from xitekInfo import ThreadInfo,PostInfo,PageInfo,ForumInfo
from xitekMongo import MongoStore

app = Flask(__name__)

@app.route('/')
def hello_world():
    #显示一个页面，该页面使用模板，并使用bootstrap
    #bootstrap文件放到static中
    return render_template("index.html")

@app.route('/forum_config')
def forum_config():
    #加载论坛列表
    #forumList=[{'forumId':1,'forumName':'体育'},{'forumId':2,'forumName':'美食'}]
    ms = MongoStore()
    ms.open()
    forumList = ms.find('forums',{})
    return render_template("forum_config.html",forumList=forumList)

@app.route('/get_forum')
def get_forum():
    forumId=request.args.get('forumId', 0)
    print(forumId)
    ms = MongoStore()
    ms.open()
    forumList = ms.find('forums',{'forumId':forumId})
    if forumList:
    
        #输出json
        return jsonify(forumList[0])
    return jsonify(ForumInfo().__dict__)

@app.route('/add_forum',methods=['POST'])
def add_forum():   
    forum = ForumInfo()
    forum.forumId=request.form['forumId']
    forum.forumName=request.form['forumName']
    forum._id=forum.forumId
    print(forum.__dict__)
    ms = MongoStore()
    ms.open()
    ms.saveForum(forum)
    return "OK"

if __name__ == '__main__':
    app.debug = True
    app.run()

