#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2014-09-02 13:08:57
# @Last Modified by:   lisnb
# @Last Modified time: 2014-09-14 13:38:29


import requests
import urllib
from bs4 import BeautifulSoup
import re
import json

def login_():
	s = requests.Session()
	with open('./config','rb') as f:
		 configs = f.read()
	configs=json.loads(configs)
	print configs['authinfo']
	print configs['headers']





def login():
	imgsrcre = re.compile(r'large:\'(.+?)\'')
	s = requests.Session()
	param = {"domain":"renren.com","email":"lisnb@sina.com","password":"5040595"}
	headers ={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"}
	t = s.post("http://www.renren.com/PLogin.do",data=param,headers = headers,allow_redirects=True)
	t = s.get('http://photo.renren.com/photo/313565854/album-437715180')
	pageinfo = BeautifulSoup(t.text.encode('utf-8'))
	anchors = pageinfo.find_all('a',class_='picture')


	for anchor in anchors:
		img = list(anchor.children)[1]
		data_info = img['data-photo']
		imgurl = imgsrcre.search(data_info).group(1)
		imgfilename = './album-437715180/'+imgurl.split('/')[-1]
		r = s.get(imgurl,stream=True)
		if r.ok:
			print 'downloading %s '%imgfilename
			with open(imgfilename,'wb') as f :
				for chunk in r.iter_content(1024):
					f.write(chunk)
		else:
			print imgfilename,'failed'


	


if __name__ == '__main__':
	login_()
