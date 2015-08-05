#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 整个过程需要的类定义 '

__author__ = 'zzyfisher'

#定义论坛
class ForumInfo:
	def __init__(self):
		self.forumId=b""
		self.forumName=""
		self.forumOther=""
		self._id=0
		
#定义一个保存帖子线索(主题)的结构
class ThreadInfo:
	def __init__(self):
		self.threadId=0
		self.title=""
		self.uid=""
		self.uname=""
		self.readNum=0
		self.replyNum=0
		self._id=0

#帖子信息结构	
class PostInfo:
	def __init__(self):
		self.threadId=0
		self.postId=0
		self.content=""
		self.uid=""
		self.uname=""
		self.postDate=""
		self._id=0

	
#定义一个分页信息的结构		
class PageInfo:
	def __init__(self):
		self.totalPage=0
		self.pageNo=0