#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2014-09-02 13:08:57
# @Last Modified by:   lisnb
# @Last Modified time: 2014-09-14 23:03:20


import requests
from bs4 import BeautifulSoup
import re
import json
import lab

def checklogin(logininfo):
	message = 'success'
	return True,message

def login():
	with open('./config','rb') as f:
		 configs = f.read()
	configs=json.loads(configs)

	print configs['authinfo']
	print configs['headers']

	s = requests.Session()
	logininfo = s.post('http://www.renren.com/PLogin.do',data = configs['authinfo'],headers=configs['headers'],allow_redirects=True)
	islogin,message = checklogin(logininfo)

	if islogin:
		return s,message
	else:
		return None,'login failed' 
	
def retrivepage():
	page = 'http://photo.renren.com/photo/313565854/album/relatives'
	session,loginmessage = login()
	if session:
		r = session.get(page)
		if r.ok:
			with open('./buffer/albums.html','wb') as f:
				f.write(r.text.encode('utf-8'))
		else:
			print 'retrive page failed'
	else:
		print message


def getfriendslist(friendid='282817208'):
	session,loginmessage = login()
	friends={}
	if session:
		getfriendlist_do = 'http://friend.renren.com/GetFriendList.do?curpage=%s&id=%s'
		friendlistinitialurl = getfriendlist_do%(0,friendid)
		friendlistinitialpage = session.get(friendlistinitialurl)
		if friendlistinitialpage.ok:
			dom = BeautifulSoup(friendlistinitialpage.text.encode('utf-8'))
			pagenumber = lab.extractfriendpagenumber(dom = dom)
			lab.extractfriendlistpage(dom,friends)
			for pn in range(1,pagenumber+1):
				print 'page %s'%pn
				pcontent = session.get(getfriendlist_do%(pn,friendid))
				if pcontent.ok:
					dom = BeautifulSoup(pcontent.text.encode('utf-8'))
					lab.extractfriendlistpage(dom,friends)
				else:
					print 'friend list page %s get failed'%pn
		else:
			print 'initial page of friend list get failed'

		with open('./buffer/%s-friends.json'%friendid,'wb') as f:
			f.write(json.dumps(friends))
	else:
		print 'get session failed'



		


def retrievephoto(session,src,localpath=''):
	if session:
		r = session.get(src,stream = True)
		if r.ok:
			with open(localpath,'wb') as f:
				for chunk in r.iter_content(1024):
					if chunk:
						f.write(chunk)
					else:
						break
		else:
			print '% :retrive failed'%src


	


if __name__ == '__main__':
	# getfriendslist()
	retrivepage()
