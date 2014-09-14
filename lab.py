#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2014-09-14 14:57:09
# @Last Modified by:   lisnb
# @Last Modified time: 2014-09-14 22:54:43



import re
from bs4 import BeautifulSoup
import util

class AlbumItemLite(object):
	"""docstring for AlbumItemLite"""
	def __init__(self):
		super(AlbumItemLite, self).__init__()
		self.id = ''
		self.name = ''
		self.description = ''
		self.thumb_src = ''
		self.thumb_local = ''
		self.photos = {}
		self.photonum=0

	def __str__(self):
		tostring = 'name:%s id:%s thumb:%s'%(self.name,self.id,self.thumb_src)
		return tostring.encode('utf-8')


class PhotoItemLite(object):
	"""docstring for PhotoItemLite"""
	def __init__(self):
		super(PhotoItemLite, self).__init__()
		self.src=''
		self.name=''
		self.local=''
		self.description = ''
	def __str__(self):
		tostring = 'name:%s description:%s'%(self.name,self.description)
		return tostring.encode('utf-8')
		

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
	
	dom = getdom() if not dom else dom

	friendinfolist = list(dom.find('ol',id='friendListCon').children)[1::2]
	#print friendinfolist
	for friendinfo in friendinfolist:
		friend = FriendItemLite()
		print friendinfo
		profile = friendinfo.p.a['href']
		friendid =  profile.split('=')[-1]
		friend.id = friendid

		friend.avatar_href = friendinfo.p.img['src']

		dds = list(friendinfo.div.find_all('dd'))
		dts = list(friendinfo.div.find_all('dt'))

		friend.name=dds[0].a.string
		if len(dts)>1 and len(dds)>1:
			friend.info_key = dts[1].string.strip() if dts[1].string else ''
			friend.info_value = dds[1].string.strip() if dds[1].string else ''

		
		print friend

		friends[friendid]=friend.__dict__

def extractfriendpagenumber(dom=None):
	dom = getdom() if not dom else dom 

	pagerdiv = dom.find(id='topPage')
	pagers = pagerdiv.find_all('a')
	lastpager = pagers[-1]
	#print lastpager
	pagenumber = util.pagerre.search(lastpager['href']).group(1)
	print pagenumber
	return int(pagenumber)

def extractalbumpagenumber(dom=None):
	dom = getdom('./buffer/album.html') if not dom else dom
	photopager_ol = dom.find('ol',id='photoPager')
	if photopager_ol:
		photopager_li = photopager_ol.find_all('li',class_='photo-pager-i')
		if photopager_li:
			return len(list(photopager_li))-1
		else:
			return 1
	else:
		return 1

def extractphotos(dom=None):
	dom = getdom('./buffer/album.html') if not dom else dom
	photohome = dom.find('div',class_='photo-list')
	# print photohome
	photolist = list(photohome.find_all('li'))
	latestphotos=[]
	for photo in photolist:
		photolite = PhotoItemLite()
		img = photo.img
		photolite.src = img['data-src']
		photolite.name = photolite.src.split('/')[-1]

		photo_info_span = photo.find('span',class_='descript')
		if photo_info_span:
			photolite.description=photo_info_span.string
		latestphotos.append(photolite.__dict__)
		print photolite
	print len(latestphotos)
	return latestphotos

def extractalbumlistpage(dom=None,albums={}):
	dom = getdom('./buffer/albums.html') if not dom else dom
	albumlist = list(dom.find('ul',id='albumListContainer'))[1::2]
	for albuminfo in albumlist:
		# print albuminfo
		album = AlbumItemLite()
		cover = albuminfo.a
		if cover:
			if cover.img:
				album.thumb_src = cover.img['data-src']
			if cover.div:
				album.photonum = int(cover.div.string.strip())
		title = albuminfo.find('a',class_='album-title')
		# print title
		if title:
			albumid = util.albumidre.search(title['href']).group(1)
			album.id = albumid
			albumname = title.find('span',class_='album-name')
			albumname = albumname.string.strip() if albumname.string else ''.join(albumname.strings)
			album.name = albumname

		print album
		albums['albumid']=album.__dict__








if __name__ == '__main__':
	extractalbumlistpage()
	#print extractalbumpagenumber()
	#extractlatestphotos()
	#extractpagenumber()
	#extractfriendlistpage()
	#fr = FriendItemLite()
	#print fr.__dict__