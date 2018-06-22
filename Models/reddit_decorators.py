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
# Contains decorator functions for the article 
# Not really necessary but I wrote it this way
# to learn about decorators
##


import arrow
import re


class RedditDecorators():
    @classmethod
    def title(_,func):
        def func_wrapper(self):
            return "# {}\n\n".format(func(self))
        return func_wrapper

    @classmethod
    def pub_date(_,func):
        def func_wrapper(self):
            pd = arrow.get(func(self))
            formatted = pd.format('YYYY-MM-DD HH:mm:ss ZZ')
            return "_Published on {}_\n\n".format(formatted)
        return func_wrapper

    @classmethod
    def mod_date(_,func):
        def func_wrapper(self):
            moddate = func(self)
            if not moddate:
                return ""
            md = arrow.get(moddate)
            formatted = md.format('YYYY-MM-DD HH:mm:ss ZZ')
            return "_Modified on {}_\n\n".format(formatted)
        return func_wrapper
    
    @classmethod
    def url_pub(_,func):
        def func_wrapper(self):
            return "###### Retrived from {}\n\n".format(func(self))
        return func_wrapper

    @classmethod
    def form_body(_,func):
        def func_wrapper(self):
            body_arr = func(self)
            resp = ""
            word_count = 0
            array_to_return = []

            for paragraph in body_arr:
                word_count += len(paragraph)
                # limit word count at 8000
                if word_count >= 8000:
                    resp += ">{}\n\n".format(paragraph)
                    array_to_return.append(resp)
                    # reset resp
                    resp = ""
                    word_count = 0
                else:
                    resp += ">{}\n\n".format(paragraph)
            array_to_return.append(resp)
            print("Total indexes "+ str(len(array_to_return)))
            return array_to_return
        return func_wrapper
    
    @classmethod
    def end_cred(_,func):
        def func_wrapper(self):
            version_no = func(self)
            source_code_md = "^(Source Code:) "
            github_md = "^[Github](https://github.com/xlanor/Minvera)"
            divider_md = " ^| "
            gitlab_md = " ^[Gitlab](https://gitlab.com/xlanor/Minvera) "
            beta_tag = " ^(_Currently in beta_ {})".format(version_no)
            return "{}{}{}{}{}".format(source_code_md,github_md,divider_md,gitlab_md,beta_tag)
        return func_wrapper
