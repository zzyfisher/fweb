#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' First Web 应用 '

from flask import Flask,render_template ,jsonify,request
from xitekInfo import ThreadInfo,PostInfo,PageInfo,ForumInfo

app = Flask(__name__)

@app.route('/')
def hello_world():
    #显示一个页面，该页面使用模板，并使用bootstrap
    #bootstrap文件放到static中
    return render_template("index.html")

@app.route('/forum_config')
def forum_config():
    #加载论坛列表
    forumList=[{'forumId':1,'forumName':'体育'},{'forumId':2,'forumName':'美食'}]
    return render_template("forum_config.html",forumList=forumList)

@app.route('/get_forum')
def get_forum():
    forumId=request.args.get('forumId', 0)
    print("收到参数：%s" %forumId)
    forum = ForumInfo()
    forum.forumId='100';
    forum.forumName="新"
    #输出json
    return jsonify(forum.__dict__)


if __name__ == '__main__':
    app.debug = True
    app.run()

