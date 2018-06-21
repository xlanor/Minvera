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
# for today articles.
##

import random
import requests
from bs4 import BeautifulSoup
import re
from .article import Article

class TodayArticle(Article):
    def __init__(self,url_link,source):
        super(TodayArticle,self).__init__(url_link,source)
        self.__todayAPI = "https://www.todayonline.com/api/v3/article/"
        self.__headers = self.__rotate_header()

    def formatArticle(self):
        self.titleProp = self.__getTitle()
        self.publishedDateProp =  self.__getPubTime()
        self.modifiedDateProp = self.__getModifiedTime()
        self.bodyProp = self.__getBody()
    
    def __getTitle(self):
        title = self.soup.find("meta",{"property":"og:title"})
        return title.attrs["content"] if title else None

    def __rotate_header(self):
        with open("./user_agents.txt") as f:
            header_list = []
            for line in f:
                header_list.append(line.rstrip('\n'))
            return {'User-Agent': random.choice(header_list)}

    def __getPubTime(self):
        pubtime = self.soup.find("meta",{"name":"cXenseParse:recs:publishtime"})
        return pubtime.attrs["content"] if pubtime else None

    def __getModifiedTime(self):
        modtime = self.soup.find("meta",{"property":"article:modified_time"})
        return modtime.attrs["content"] if modtime else None

    def __getBody(self):
        artid = self.soup.find("meta", { "name" : "cXenseParse:recs:articleid" })

        api = "{}{}".format(self.__todayAPI,artid.attrs["content"])

        r = requests.get(api,headers = self.__headers)
        js = r.json()
        story = js["node"]["body"]
        story.rstrip('\r\n')
        story = BeautifulSoup(story,'html.parser')
        array_of_paras = story.findAll("p")
        return_arr = [i.text for i in array_of_paras]
        return return_arr