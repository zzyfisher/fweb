#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' First Web 应用 '

from flask import Flask,render_template ,jsonify,request
from celery import Celery
from celery.task import task
from scanner.po import ThreadInfo,PostInfo,PageInfo,ForumInfo
from mongo_store import MongoStore
from web.task_forum import scan_forum_task


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


#进入爬论坛相关的页面
@app.route('/forum_fetch',methods=['GET'])
def forum_fetch():
    return render_template("forum_fetch.html")
	
#获取当前执行的爬虫列表
@app.route('/forum/running',methods=['GET'])
def forum_running():
    list=[]
    for i in range(1,3):
        r = ForumInfo()
        r.forumId=i
        r.forumName='name for ' + str(i)
        list.append(r)
    return jsonify(list[0].__dict__)




#启动任务
@app.route('/forum/start/<forumId>',methods=['GET'])
def forum_start(forumId):
    task = scan_forum_task.apply_async(args=[10])
    return {'taskId':task.id}
    



@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = scan_forum_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        #job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.debug = True
    app.run()