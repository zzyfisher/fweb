#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 主程序 '

from xitekInfo import ThreadInfo,PostInfo,PageInfo,ForumInfo
from xitekThread import XitekThreadParser
from xitekForum import XitekForumParser
from xitekMongo import MongoStore

#准备数据库
ms = MongoStore()
ms.open()

#执行抓取论坛主题
class ProcessForum():
	def process(self,forumId,batchId):
		
		#遍历一个forum
		pageNum =1
		forumParser =  XitekForumParser(forumId)
		pageData= forumParser.fetchPage(pageNum)
		ret = forumParser.parsePage(pageData)
		threadList = ret[0]
		pageInfo = ret[1]

		print("****第%s页****"%pageNum)
		for p in threadList:
			#print (p.threadId+","+p.title+","+p.uid+","+p.uname+","+p.replyNum+"," + p.readNum)
			p.batchId=batchId
			ms.saveThread(p)

		#for num in range(2, int(pageInfo.totalPage)-301):
		for num in range(2, 3):
			pageData= forumParser.fetchPage(num)
			ret = forumParser.parsePage(pageData)
			threadList = ret[0]
			pageInfo = ret[1]

			print("****第%s页****"%num)
			for p in threadList:
				#print (p.threadId+","+p.title+","+p.uid+","+p.uname+","+p.replyNum+"," + p.readNum)
				p.batchId=batchId
				ms.saveThread(p)

#处理一个论坛线索
class ProcessThread():
	def process(self,forumId,batchId):
		#取出batchId所有未处理过的Thread
		listThread=ms.find('threads',{'forumId':forumId,'batchId':batchId})
		#遍历这些thread
		for t in listThread:
			print(t)
			#抓取每个thread
			tp = XitekThreadParser(t['threadId'])
			pageData = tp.fetchPage(1)
			ret=tp.parsePage(pageData,1)
			listPost=ret[0]
			maxPage = ret[1]
			#遍历保存
			for p in listPost:
				p.batchId=batchId
				ms.savePost(p)
			#处理其他页
			for num in range(2, maxPage+1):
				pageData = tp.fetchPage(num)
				ret=tp.parsePage(pageData,num)
				listPost=ret[0]				
				#遍历保存
				for p in listPost:
					p.batchId=batchId
					ms.savePost(p)

		
if __name__=='__main__':
	pf = ProcessThread()
	pf.process(103,'A-01')
