#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import re

class BaseHandler(tornado.web.RequestHandler):

    @property
    def mysql_pool(self):
        return self.application.mysql_pool