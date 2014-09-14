#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2014-09-14 16:24:19
# @Last Modified by:   lisnb
# @Last Modified time: 2014-09-14 22:34:20


import re

pagerre = re.compile(r'curpage=(\d*)')
albumcoverre = re.compile(r'url:(.+)')
albumidre = re.compile(r'album-(\d+)\?')