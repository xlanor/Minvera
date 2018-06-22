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
# Main method
##

import praw
import os
import re
import sys
import json
from Controllers.ScrapeFactory import ScrapeFactory
from Models.exception_handlers import Failables
from Models.exceptions import *
import time

class RedditBot():
    def __init__(self,reddit,subreddit):
        self.__reddit = reddit
        self.__subreddit = subreddit
        self.__st_login = None
        self.__postReplied = None

    @property
    def subRedditProp(self):
        return self.__subreddit
    
    @property
    def redditProp(self):
        return self.__reddit

    @property
    def st_details(self):
        return self.__st_login
    
    @st_details.setter
    def st_details(self,loginDict):
        self.__st_login = loginDict

    @property
    def listOfRepliedPost(self):
       return self.__postReplied
    
    @listOfRepliedPost.setter
    def listOfRepliedPost(self,fileName):
        if not os.path.isfile(fileName):
            self.__postReplied = []
        else:
            self.__postReplied = []
            with open (fileName) as f:
                for line in f:
                    self.__postReplied.append(line.rstrip('\n'))

    @Failables.known_exceptions
    def checkSubmission(self):
        for submission in self.subRedditProp.new(limit=30):
            print ("Checking submission "+submission.id)
            if submission.id not in self.listOfRepliedPost:
                # if re.search("straitstimes.com",submission.url,re.IGNORECASE):
                #    print("Sumission ID "+submission.id +" is of type Straits Times")
                url = submission.url.split('?')[0]
                self.__executeRipPost(url,submission)
        time.sleep(300)

    @Failables.known_exceptions
    def __executeRipPost(self,url,submission):
        commentArray = ScrapeFactory.getScrapeType(self.st_details,url)
        # commentArray = self.__getArticle(url)
        if commentArray:
            self.__postComment(commentArray,submission)
            self.__addReplied(submission.id)

    def __postComment(self,commentArray,submission):
        count = 0
        if len(commentArray) > 1:
            c = submission.reply(commentArray[0])
            for comment in commentArray:
                if count == 0: pass
                else:
                    time.sleep(5) 
                    c = c.reply(comment)
                count += 1

        else:
            time.sleep(5) 
            submission.reply(commentArray[0])
    
    def __addReplied(self,sub_id):
        self.__postReplied.append(sub_id)
        with open("posts_replied_to.txt","a+") as postFile:
            postFile.write(sub_id)
            postFile.write("\n")


if __name__ == "__main__":
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('testing_st+singapore')
    r = RedditBot(reddit,subreddit)
    print("Instantiating new praw")
    r.listOfRepliedPost = "posts_replied_to.txt"
    with open('login_details.json') as logind:
        data = json.load(logind)
        try:
            user = data['st']
            login = user['username']
            password = user['password']
            r.st_details = {'user':login,'password':password}
            print ("Login details loaded")
        except KeyError as k:
            print("Missing Keys")
            sys.exit()
        except Exception as e:
            print ("Unknown Exception")
            sys.exit()
        else:
            while True:
                r.checkSubmission()
                time.sleep(400)