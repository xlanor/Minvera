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
#  Decorator for exceptions
##
from .exceptions import *
from urllib.error import HTTPError
from prawcore.exceptions import ResponseException
from arrow.parser import ParserError

class Failables():
    @classmethod
    def known_exceptions(_,func):
        def func_wrapper(*args):
            try:
                return func(*args)
            except HTTPError as e:
                print("HTTP Error, not loaded")
                pass
            except AttributeError as a:
                print("Attribute error, not loaded")
                raise NoAttributesFound("Attribute error, not loaded")
            except NoAttributesFound as naf: 
                print("No Attributes error caught")
                pass
            except ResponseException as re:
                print("Reddit timed, pass")
                pass
            
        return func_wrapper

    @classmethod
    def formatting_exceptions(_,func):
        def func_wrapper(*args):
            try:
                return func(*args)
            except ParserError as pe:
                return ""
            except AttributeError as a:
                return ""
            except TypeError:
                raise NoAttributesFound("No Attributes found")
        return func_wrapper
