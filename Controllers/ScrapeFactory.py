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
#  Factory Pattern to determine which Model to take.
##
import re
from Models.exception_handlers import Failables
from .scrape import openSite
from .scrape import STLogin
from Models.st_article import StArticle
from Models.today_article import TodayArticle
from Models.cna_article import CnaArticle
from Models.tnp_article import TnpArticle
from Models.asiaone_article import AsiaOneArticle


class ScrapeFactory():

    @staticmethod
    @Failables.known_exceptions
    def getScrapeType(st_login,url):
        if re.search(r'(straitstimes.com|todayonline.com|channelnewsasia.com|tnp.sg|asiaone.com)',url,re.IGNORECASE):
            print("Getting article from "+url)
            s = openSite(url).request_source()
        isRetrieved = False
        if re.search("straitstimes.com",url,re.IGNORECASE):
            retrivedArt = StArticle(url,s)
            retrivedArt.formatArticle()
            if retrivedArt.premProp:
                print("Premium article, logging in")
                s = STLogin(url,st_login["user"],st_login["password"]).attemptLogin() # premium
                retrivedArt = StArticle(url,s)
                retrivedArt.formatArticle()
            isRetrieved = True

        elif re.search("todayonline.com",url,re.IGNORECASE):
            retrivedArt = TodayArticle(url,s)
            retrivedArt.formatArticle()
            isRetrieved = True

        elif re.search("channelnewsasia.com",url,re.IGNORECASE):
            
            retrivedArt = CnaArticle(url,s)
            retrivedArt.formatArticle()
            isRetrieved = True

        elif re.search("tnp.sg",url,re.IGNORECASE):
            retrivedArt = TnpArticle(url,s)
            retrivedArt.formatArticle()
            isRetrieved = True
        
        elif re.search("asiaone.com",url,re.IGNORECASE):
            retrivedArt = AsiaOneArticle(url,s)
            retrivedArt.formatArticle()
            isRetrieved = True

        if isRetrieved:
            articleArray = retrivedArt.returnArticle()
            return articleArray
        else:
            return None
