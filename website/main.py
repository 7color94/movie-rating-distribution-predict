#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado_mysql import pools
from urls import handlers
import MySQLdb

version = sys.version_info[0]
if version < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

define('port', default=9600, help='run tornado app on the given port', type=int)


class App(tornado.web.Application):
    def __init__(self):
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            cookie_secret = "ajkfdlkfkdsofidsofjohsdk;eoport",
            autoescape = None,
            xsrf_cookies = True,
            debug = True,
            login_url = "/signin",
        )
        super(App, self).__init__(handlers, **settings)
        self.db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='1227401054', db='mrp', charset="utf8")
        self.mysql_pool = pools.Pool(dict(host='127.0.0.1', port=3306, user='root', passwd='1227401054', db='mrp', charset="utf8"), max_idle_connections=5, max_open_connections=10)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()