#! /usr/bin/env python
# -*- coding: utf-8 -*-
# By i@BlahGeek.com at 08/16/2013

from datetime import timedelta
from os import path

FEEDS_URL = (
        'http://www.guokr.com/rss/', 
        'http://solidot.org.feedsportal.com/c/33236/f/556826/index.rss', 
        'http://ppwwyyxx.com/atom.xml', 
        'https://zh.greatfire.org/news/blog/rss', 
        'http://fullrss.net/a/http/news.163.com/special/00011K6L/rss_newstop.xml', 
        'https://www.archlinux.org/feeds/news/', 
        'http://capbone.com/feed/', 
        'http://www.36kr.com/feed', 
        'http://www.guao.hk/feed', 
        )

KINDLEGEN = '/usr/bin/kindlegen'

MAXOLD = timedelta(days=1)

ROOT = path.dirname(path.abspath(__file__))
OUTPUTDIR = path.join(ROOT, 'output')
