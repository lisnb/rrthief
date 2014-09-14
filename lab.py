#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2014-09-14 14:57:09
# @Last Modified by:   lisnb
# @Last Modified time: 2014-09-14 16:18:11



import re
from bs4 import BeautifulSoup


class FriendItemLite(object):
	"""docstring for FriendItemLite"""
	def __init__(self):
		super(FriendItemLite, self).__init__()
		self.id = ''
		self.avatar_href = ''
		self.avatar_local = ''
		self.name = ''
		self.info_key = ''
		self.info_value = ''
	def __str__(self):
		# tostring = 'name:%s id:%s avatar_href:%s avatar_local:%s info_key:%s info_value:%s'%(   self.name,
		# 																						self.id,
		# 																						self.avatar_href,
		# 																						self.avatar_local,
		# 																						self.info_key,
			
		tostring = 'name:%s id:%s info_key:%s info_value:%s'%(  self.name,
																self.id,
																self.info_key,
																self.info_value)
		return tostring.encode('utf-8')

def getdom(page='./buffer/282817208-friendlistinitialpage.html'):
	with open(page,'rb') as f:
		content = f.read()

	dom = BeautifulSoup(content)
	return dom

def extractfriendlistpage(dom=None,friends={}):
	
	dom = getdom()

	friendinfolist = list(dom.find(id='friendListCon'))[1::2]
	for friendinfo in friendinfolist:
		friend = FriendItemLite()

		profile = friendinfo.p.a['href']
		friendid =  profile.split('=')[-1]
		friend.id = friendid

		friend.avatar_href = friendinfo.p.img['src']

		dds = list(friendinfo.div.find_all('dd'))
		dts = list(friendinfo.div.find_all('dt'))

		friend.name=dds[0].a.string
		friend.info_key = dts[1].string.strip()
		friend.info_value = dds[1].string.strip()

		
		print friend

def extractpagenumber(dom=None):
	dom = getdom()

	pagerdiv = dom.find(id='topPage')
	pagers = pagerdiv.find_all('a')
	lastpager = pagers[-1]
	print lastpager


	




if __name__ == '__main__':
	extractpagenumber()
	# extractfriendlistpage()
	#fr = FriendItemLite()
	#print fr.__dict__