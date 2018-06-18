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
##

from bs4 import BeautifulSoup
import re
from .article import Article

class StArticle(Article):
    def __init__(self,url_link,source):
        super(StArticle,self).__init__(url_link,source)
    
    def formatArticle(self):
        self.titleProp = self.__getTitle()
        self.publishedDateProp =  self.__getPubTime()
        self.modifiedDateProp = self.__getModifiedTime()
        self.bodyProp = self.__getBody()
        self.premProp = self.__isPremium()
    
    def __getTitle(self):
        title = self.soup.find("meta",{"property":"og:title"})
        return title.attrs["content"] if title else None

    def __getPubTime(self):
        pubtime = self.soup.find("meta",{"property":"article:published_time"})
        return pubtime.attrs["content"] if pubtime else None

    def __getModifiedTime(self):
        modtime = self.soup.find("meta",{"property":"article:modified_time"})
        return modtime.attrs["content"] if modtime else None

    def __isPremium(self):
        premString = "You have reached one of our Premium stories. To continue reading, get access now or log in if you are a subscriber"
        for body in self.bodyProp:
            if re.search(premString,body,re.IGNORECASE):
                return True
        return False

    def __getBody(self):
        bodyText = self.soup.find("div", { "class" : "odd field-item" })
        # should only be one...
        # extraction f paragraphs
        p = bodyText.findAll('p',{"class": None, "dir": None})
        # reconstructs the array with stripped text.
        # done to ensure we can wrap it later with a decorator
        # we might want to use this for telegram later so we
        # dont leave this strictly as reddit, so that we can
        # modularize it if need be
        bodyArray = []
        for para in p:
            blockquote = para.findAll('blockquote')
            fig = para.findAll('figure')
            # decompose twitter
            for b in blockquote:
                b.decompose()
            # decomposes images
            for f in fig:
                f.decompose()
            remaining_text = para.text
            # Stripping characters
            remaining_text = remaining_text.replace(u'\xa0', u' ')
            # Removes the st email
            if remaining_text != "stopinion@sph.com.sg" and remaining_text:  
                bodyArray.append(remaining_text) 

        return bodyArray if len(bodyArray) > 0 else None