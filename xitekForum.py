#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 处理一个论坛 '

from bs4 import BeautifulSoup
from urllib import request
import re

from xitekInfo import ThreadInfo,PostInfo,PageInfo,ForumInfo
#处理论坛的帖子列表
class XitekForumParser:
	def __init__(self,forumId):
		self.forumId=forumId
		self.url="http://forum.xitek.com/forum-[forum]-[page].html"
		
	#抓取第p页
	def fetchPage(self,pageNum):
		purl = self.url.replace("[page]",str(pageNum))
		purl = purl.replace("[forum]",str(self.forumId))
		print("Fetching(%s)..."%purl)
		with request.urlopen(purl) as f:
			data = f.read()
			#print('Status:', f.status, f.reason)
			#for k, v in f.getheaders():
			#	print('%s: %s' % (k, v))
			return data.decode('gbk')


	#解析一个页
	#返回当前页的帖子列表结构，以及当前页号，总页号
	def parsePage(self,data):
		'''
		<tbody id="normalthread_1466792" >
			<tr>
			<td class="icn">
			<a href="thread-1466792-1-1-1.html" title="新窗口打开" target="_blank">

			<img src="static/image/common/hot_3.gif" align="热帖" />
			</a>
			</td>
			<th class="new">
			 <a href="thread-1466792-1-1-1.html"  onclick="atarget(this)" class="xst">夏天到了</a>
			<img src="static/image/filetype/common.gif" alt="attachment" title="附件" align="absmiddle" />
			                      <font size=2>47</font>                             </th>
			<td class="by1 xi2">
			<a href="/space-uid-2117226.html" style='color:#000' c="1">山中问答</a></td>
			<td class="num1 xi2">879</td>
			<td class="num2 xi2">89054</td>
			<td class="by2 xi2" nowrap>
			筋肉 <font color=#800080>8-04 08:51</font>
			</td>
			</tr>
		</tbody>
		'''
		soup = BeautifulSoup(data,"html.parser")
		tablelist=soup.find_all("tbody",id=re.compile('^normalthread_'))
		
		retList=[]

		for t in tablelist:
			#使用正则获取帖子列表中的值
			#thread-id,title,uid,uname,回帖，阅读
			pattern = re.compile(r'<th class=.*?<a .*?thread-(.*?)-.*?.html.*?>(.*?)</a>.*?</th>'\
				'.*?<a .*?space-uid-(.*?).html.*?>(.*?)</a>.*?<td .*?>(.*?)</td>.*?<td .*?>(.*?)</td>',re.S)
			msg=t.prettify()
			#print(msg)
			v=re.findall(pattern,msg)
			#print(v)

			r=ThreadInfo();
			r.forumId=self.forumId
			r.threadId=v[0][0].strip()
			r._id=r.threadId
			r.title = v[0][1].strip()
			r.uid=v[0][2].strip()
			r.uname=v[0][3].strip()
			r.replyNum=v[0][4].strip()
			r.readNum=v[0][5].strip()

			retList.append(r)			

		#处理页数量
		#<a href="forum-50-400.html" class="last">... 400</a>
		lastPage=soup.find("a",attrs={"class":"last"})		
		href =lastPage.get('href')

		#解析一下页数量
		#forum-id,last-page-number
		pattern = re.compile(r'forum-(.*?)-(.*?).html',re.S)
		pagenum= re.findall(pattern,href)
		#print(pagenum)

		page = PageInfo()
		page.totalPage=pagenum[0][1].strip()
		page.pageNo = 0
		page.forumId=pagenum[0][0].strip()

		return (retList,page)

if __name__=='__main__':
	#论坛编号
	forumId=103
	#遍历一个forum
	pageNum =1
	forumParser =  XitekForumParser(forumId)
	pageData= forumParser.fetchPage(pageNum)
	ret = forumParser.parsePage(pageData)
	threadList = ret[0]
	pageInfo = ret[1]

	print("****第%s页****"%pageNum)
	for p in threadList:
		print (p.threadId+","+p.title+","+p.uid+","+p.uname+","+p.replyNum+"," + p.readNum)

	for num in range(2,5):
		pageData= forumParser.fetchPage(num)
		ret = forumParser.parsePage(pageData)
		threadList = ret[0]
		pageInfo = ret[1]

		print("****第%s页****"%num)
		for p in threadList:
			print (p.threadId+","+p.title+","+p.uid+","+p.uname+","+p.replyNum+"," + p.readNum)

	print("#######")