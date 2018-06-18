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
# Article superclass for... articles?
##

from .reddit_decorators import RedditDecorators


class Article():
    def __init__(self,url_link,source):
        self.__title = None
        self.__author = None
        self.__published_date = None
        self.__modified_date = None
        self.__body = None
        self.soup = source
        self.isLonger = False  # Is Longer than reddit?
        self.__urlLink = url_link
        self.isPremium = False

    @property
    @RedditDecorators.title
    def titleProp(self):
        return self.__title

    # Currently unused
    def __getAuthor(self):
        return self.__author

    @property
    @RedditDecorators.pub_date
    def publishedDateProp(self):
        return self.__published_date

    @property
    @RedditDecorators.mod_date
    def modifiedDateProp(self):
        return self.__modified_date

    @property
    @RedditDecorators.form_body
    def bodyProp(self):
        return self.__body

    @property
    @RedditDecorators.url_pub
    def urlLinkProp(self):
        return self.__urlLink

    @property
    def checkLongerProp(self):
        return self.isLonger
    
    @property
    def premProp(self):
        return self.isPremium

    @bodyProp.setter
    def bodyProp(self,body):
        self.__body = body

    @titleProp.setter
    def titleProp(self,title):
        self.__title = title

    # Currently unused
    def setAuthor(self, auth):
        self._author = auth

    @publishedDateProp.setter
    def publishedDateProp(self, pd):
        self.__published_date = pd

    @modifiedDateProp.setter
    def modifiedDateProp(self,md):
        self.__modified_date = md

    @urlLinkProp.setter
    def urlLinkProp(self,url):
        self.__urlLink = url
        
    @premProp.setter
    def premProp(self,result):
        self.isPremium = result

    def returnArticle(self):
        count = 0
        returnArray = []
        for post in self.bodyProp:
            if count == 0:
                stringToAppend = "{}{}{}{}".format(self.titleProp,self.publishedDateProp,
                                                  self.modifiedDateProp,post
                                                  )
                returnArray.append(stringToAppend)
            else:
                returnArray.append(post)
            count += 1
        last_post = returnArray[len(returnArray)-1]
        returnArray[len(returnArray)-1] = "{}{}".format(last_post,self.urlLinkProp)

        return returnArray