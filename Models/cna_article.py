#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Minvera
# Copyright (C) 2018 xlanor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
# sublcass of Article superclass
# for CNA articles.
##

import random
import requests
from bs4 import BeautifulSoup
import re
from .article import Article

class CnaArticle(Article):
    def __init__(self,url_link,source):
        super(CnaArticle,self).__init__(url_link,source)
        print("New cna object initalized")

    def formatArticle(self):
        self.titleProp = self.__getTitle()
        self.publishedDateProp =  self.__getPubTime()
        self.modifiedDateProp = self.__getModifiedTime()
        self.bodyProp = self.__getBody()
    
    def __getTitle(self):
        title = self.soup.find("meta",{"property":"og:title"})
        return title.attrs["content"] if title else None

    def __getPubTime(self):
        pubtime = self.soup.find("meta",{"name":"cXenseParse:recs:publishtime"})
        return pubtime.attrs["content"] if pubtime else None

    def __getModifiedTime(self):
        modtime = self.soup.find("meta",{"property":"article:modified_time"})
        return modtime.attrs["content"] if modtime else None

    def __getBody(self):
        paras = self.soup.findAll('p',{"class": None})
        body_arr = []
        for para in paras:
            blockquote = para.findAll('blockquote')
            fig = para.findAll('figure')
            dv = para.findAll('div')
            # decompose twitter
            for b in blockquote:
                b.decompose()
            # decomposes images
            for f in fig:
                f.decompose()
            for d in dv:
                d.decompose()
            para_string = para.text.replace('\n','')
            if  para_string:
                body_arr.append(para_string.lstrip())
                
        return body_arr if len(body_arr) > 0 else None