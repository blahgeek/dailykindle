#! /usr/bin/env python
# -*- coding: utf-8 -*-
# By i@BlahGeek.com at 08/16/2013

from datetime import timedelta
from os import path

FEEDS_URL = (
        'http://www.guokr.com/rss/', 
        'http://solidot.org.feedsportal.com/c/33236/f/556826/index.rss', 
        'http://cnbeta.feedsportal.com/c/34306/f/624776/index.rss', 
        'http://ppwwyyxx.com/atom.xml', 
        )

KINDLEGEN = '/usr/bin/kindlegen'

MAXOLD = timedelta(days=1)

ROOT = path.dirname(path.abspath(__file__))
OUTPUTDIR = path.join(ROOT, 'output')
