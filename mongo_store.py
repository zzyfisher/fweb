#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 操作mongo '
__author__ = 'zzyfisher'
import json
from pymongo import MongoClient
import time

#from scanner.xitekInfo import ThreadInfo,PostInfo,PageInfo,ForumInfo
	
class MongoStore:
	#构造
	def __init__(self):		
		self.conn=b""
		self.db=b""
		
	#打开db
	def open(self):
		self.conn = MongoClient("127.0.0.1",27017)
		self.db = self.conn.xitek
		
	#保存到db-thread（主题）
	def saveThread(self,thread):
		j= json.dumps(thread, default=lambda thread: thread.__dict__)
		self.db.threads.save(json.loads(j))
	def saveForum(self,forum):
		j= json.dumps(forum, default=lambda forum: forum.__dict__)
		print(j)
		self.db.forums.save(json.loads(j))
	def savePost(self,post):
		j= json.dumps(post, default=lambda post: post.__dict__)
		self.db.posts.save(json.loads(j))

	def find(self,table,exp):
		return self.db[table].find(exp)	
		

	
