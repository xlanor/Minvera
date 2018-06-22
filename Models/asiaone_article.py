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
# for asiaone articles
##

from bs4 import BeautifulSoup
import re
from .article import Article

class AsiaOneArticle(Article):
    def __init__(self,url_link,source):
        super(AsiaOneArticle,self).__init__(url_link,source)
    
    def formatArticle(self):
        self.titleProp = self.__getTitle()
        self.publishedDateProp =  self.__getPubTime()
        self.modifiedDateProp = self.__getModifiedTime()
        self.bodyProp = self.__getBody()
    
    def __getTitle(self):
        title = self.soup.find("meta",{"property":"og:title"})
        return title.attrs["content"] if title else None

    def __getPubTime(self):
        pubtime = self.soup.find("meta",{"property":"og:article:published_time"})
        return pubtime.attrs["content"] if pubtime else None

    def __getModifiedTime(self):
        return "-"

    def __getBody(self):
        article_div = self.soup.find('div',{'class':'field field-name-body'})
        paragraphs = article_div.findAll('p')
        text_arr = []
        for p in paragraphs:
            remaining_text = p.text
            remaining_text = remaining_text.replace(u'\xa0', u' ')
            if remaining_text:
                text_arr.append(remaining_text)

        return text_arr if len(text_arr) > 0 else None