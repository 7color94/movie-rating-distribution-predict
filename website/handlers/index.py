#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time

import tornado.web
from tornado import gen
import tornado_mysql

from . import BaseHandler
from entity import newMovie, votesMovie


class IndexHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        page = int(self.get_argument('page', 1))
        cur = yield self.mysql_pool.execute("SELECT count(*) FROM new_movies")
        counts = cur.fetchone()[0]
        cur.close()
        pages = counts/20
        if pages*20 < counts:
            pages += 1
        if page > pages:
            page = pages
        start = 20*(page-1)
        cur = yield self.mysql_pool.execute("SELECT * FROM new_movies LIMIT %s,%s", (start, 20))
        new_movie_list = []
        for result in cur:
            nMovie = newMovie()
            nMovie.id = result[0]
            nMovie.title = result[1]
            nMovie.director = result[13]
            nMovie.poster_url = result[20]
            new_movie_list.append(nMovie)
        cur.close()
        self.render(
            'index.html',
            new_movie_list = new_movie_list,
            page = page,
            pages = pages,
            pagination_flag = 1,
            )


class NewMovieHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self, movie_id):
        cur = yield self.mysql_pool.execute("SELECT * FROM new_movies WHERE id=%s", (movie_id,))
        result = cur.fetchone()
        nMovie = newMovie()
        nMovie.id = result[0]
        nMovie.title = result[1]
        nMovie.color = result[2]
        nMovie.genre = result[3]
        nMovie.language = result[4]
        nMovie.soundmix = result[5]
        nMovie.country = result[6]
        nMovie.cast = result[7]
        nMovie.producer = result[8]
        nMovie.writer = result[9]
        nMovie.cinematographer = result[10]
        nMovie.composer = result[11]
        nMovie.costume_designer = result[12]
        nMovie.director = result[13]
        nMovie.editor = result[14]
        nMovie.company = result[15]
        nMovie.year = result[16]
        nMovie.running_time = result[17]
        nMovie.keywords = result[18]
        nMovie.imdb_url = result[19]
        nMovie.poster_url = result[20]
        cur.close()
        self.render(
            'moviedetail.html',
            new_movie = nMovie,
            )


class NewMovieRatingHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self, movie_id):
        cur = yield self.mysql_pool.execute("SELECT * FROM new_movies_voting WHERE id=%s", (movie_id,))
        vMovie = votesMovie()
        result = cur.fetchone()
        vMovie.id = result[0]
        vMovie.votes_one = result[1]
        vMovie.votes_two = result[2]
        vMovie.votes_three = result[3]
        vMovie.votes_four = result[4]
        vMovie.votes_five = result[5]
        vMovie.votes_six = result[6]
        vMovie.votes_seven = result[7]
        vMovie.votes_eight = result[8]
        vMovie.votes_nine = result[9]
        vMovie.votes_ten = result[10]
        cur.close()
        cur = yield self.mysql_pool.execute("SELECT title, imdb_url, poster_url FROM new_movies WHERE id=%s", (movie_id,))
        result = cur.fetchone()
        vMovie.title = result[0]
        vMovie.imdb_url = result[1]
        vMovie.poster_url = result[2]
        self.render(
            'newmovierating.html',
            votes_movie = vMovie,
            )

class SearchHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        to_search_name = self.get_argument('q')
        cur = yield self.mysql_pool.execute("SELECT * FROM new_movies WHERE title like %s", ('%'+to_search_name+'%'))
        new_movie_list = []
        for result in cur:
            nMovie = newMovie()
            nMovie.id = result[0]
            nMovie.title = result[1]
            nMovie.director = result[13]
            nMovie.poster_url = result[20]
            new_movie_list.append(nMovie)
        cur.close()
        self.render(
            'index.html',
            new_movie_list = new_movie_list,
            pagination_flag = 0,
            )


handlers = [
    (r"/", IndexHandler),
    (r"/new-movie/(\d+)", NewMovieHandler),
    (r"/new-movie-rating/(\d+)", NewMovieRatingHandler),
    (r"/search/", SearchHandler),
]