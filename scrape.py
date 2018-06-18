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
# Scraper Module
##
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import os
import time
import requests
from bs4 import BeautifulSoup
from Models.st_article import StArticle


class openSite():
    def __init__(self,url):
        self.url = url
        self.driver = None
        # Chromedriver uses the installed chrome.
        self.__chrome_driver = "./chromedriver"
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def loadDriver(self):
        driver = webdriver.Chrome(chrome_options=self.__chrome_options(), executable_path=self.__chrome_driver)
        driver.get(self.url)
        driver.get_screenshot_as_file("capture0.png")
        return driver

    def __chrome_options(self):
        # instantiate a chrome options object so you can set the size and headless preference
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")
        return chrome_options
    
    def request_source(self):
        r = requests.get(self.url,headers = self.__headers)
        soup = BeautifulSoup(r.content,'html.parser')
        return soup


class STLogin(openSite):
    def __init__(self,url,username,password):
        super(STLogin,self).__init__(url)
        self.driver = openSite.loadDriver(self)
        self.__username = username
        self.__password = password
        self.__login_url = "https://www.straitstimes.com/p/redirect.php?q=https%3A%2F%2Fwww.straitstimes.com%2F%3Floggedout%3Dtrue"

    def __close_driver(self):
        self.driver.close()

    def __login_Attempt(self):
        self.driver.get(self.__login_url)
        time.sleep(5)
        self.driver.get_screenshot_as_file("at_page.png")
        user = self.driver.find_element_by_name('j_username')
        pw = self.driver.find_element_by_name('j_password')
        # loginbtn = self.driver.find_element_by_xpath("//input[@id='login']")
        loginbtn = self.driver.find_element_by_name('j_password')

        user.send_keys(self.__username)
        pw.send_keys(self.__password)
        loginbtn.send_keys(Keys.TAB)
        loginbtn.send_keys(Keys.TAB)
        loginbtn.send_keys(Keys.TAB)
        loginbtn.send_keys(Keys.ENTER)
        #loginbtn.click()
        time.sleep(10)
        self.driver.get_screenshot_as_file("capture.png")
        self.driver.get(self.url)
        time.sleep(10)
        self.driver.get_screenshot_as_file("capture2.png")
        #self.driver.close()
        try:
            self.driver.find_element_by_xpath("//input[@id='login']")
        except NoSuchElementException:
            return True
        else:
            return False

    def attemptLogin(self):
        if self.__login_Attempt():
            print("Logged in")
            return self.request_source()
        else:
            print("Not Logged in")
    
    def request_source(self):
        
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        return soup

if __name__ == "__main__":
    print("Init")
