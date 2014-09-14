#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2014-09-14 00:46:02
# @Last Modified by:   lisnb
# @Last Modified time: 2014-09-14 01:43:15

from bs4 import BeautifulSoup
import re



def foo():
	with open('./buffer.html','rb') as f:
		html = f.read()

	imgsrcre = re.compile(r'large:\'(.+?)\'')


	pageinfo = BeautifulSoup(html)
	picturewall = pageinfo.find_all('a',class_='picture')
	imgs = picturewall#filter(lambda x:'picture' in x.get('class',[]) , picturewall)
	print len(imgs)
	for img in imgs:
		imageinfo = list(img.children)[1]['data-photo']
		print imgsrcre.search(imageinfo).group(1).split('/')[-1]

	#print len(picturewall),type(picturewall[0])


if __name__ == '__main__':
	foo()