# -*- coding: utf-8 -*-
# python36
__author__ = 'wuqili'
import os
import sys
from scrapy.cmdline import execute

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
execute(["scrapy", "crawl", "zhihu_live"])