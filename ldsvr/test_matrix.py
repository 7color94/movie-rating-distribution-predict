#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import MySQLdb
import numpy as np
from entity import newMovie

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '1227401054'
mysql_db = 'mrp'
conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset="utf8")

redis_ip = 'localhost'
redis_port = 6379
redis_key_indexing_pre = 'mrp:'
redis_key_indexing_suf = ':indexing'
r = redis.Redis(host=redis_ip, port=redis_port)

m = 0
d = 0
x = None
x_row_index = 0
test_id_matrix = None

max_year = 0.0
min_year = 9999.0
min_running_time = 9999.0
max_running_time = 0.0

features = [
    'color', 'genre', 'language', 
    'soundmix', 'country', 
    'actor', 'actress', 'producer', 
    'writer', 'cinematographer', 'composer', 
    'costume designer', 'director', 'editor', 
    'company', 'year', 'running time'
]


def test_matrix_init():
    cur = conn.cursor()
    global x
    global test_id_matrix
    global m
    global d
    global max_year
    global min_year
    global min_running_time
    global max_running_time
    d=0
    # cal d
    for f in features:
        f_keys = r.hkeys(redis_key_indexing_pre+f+redis_key_indexing_suf)
        d += len(f_keys)
    # cal m
    count = cur.execute('SELECT count(*) FROM new_movies')
    m = cur.fetchone()[0]
    x = np.zeros((m, d), dtype=np.double)
    test_id_matrix = np.zeros((m, 1), dtype=np.int)
    print "testFeature's size: ", x.shape
    max_year = (int)(r.get('mrp:max_year'))
    min_year = (int)(r.get('mrp:min_year'))
    max_running_time = (int)(r.get('mrp:max_running_time'))
    min_running_time = (int)(r.get('mrp:min_running_time'))
    print max_year, min_year
    print max_running_time, min_running_time
    cur.close()


def debug_x():
    for r in x[0:1]:
        print r


def set_column_value(key, info):
    global x_row_index
    global x
    column_index = None
    if r.hexists(redis_key_indexing_pre + key + redis_key_indexing_suf, info.lower()):
        column_index = r.hget(redis_key_indexing_pre + key + redis_key_indexing_suf, info.lower())
    else:
        column_index = r.hget(redis_key_indexing_pre + key + redis_key_indexing_suf, key.lower()+':others')
    # print 'find: ', key, info, column_index
    x[x_row_index, column_index] = 1
    # print 'set: ', x_row_index, column_index
    # debug_x()


def set_cast_column_value(info):
    global x_row_index
    global x
    column_index = None
    if r.hexists(redis_key_indexing_pre + 'actor' + redis_key_indexing_suf, info.lower()):
        column_index = r.hget(redis_key_indexing_pre + 'actor' + redis_key_indexing_suf, info.lower())
    else:
        column_index = r.hget(redis_key_indexing_pre + 'actor' + redis_key_indexing_suf, 'actor'.lower()+':others')
    x[x_row_index, column_index] = 1
    if r.hexists(redis_key_indexing_pre + 'actress' + redis_key_indexing_suf, info.lower()):
        column_index = r.hget(redis_key_indexing_pre + 'actress' + redis_key_indexing_suf, info.lower())
    else:
        column_index = r.hget(redis_key_indexing_pre + 'actress' + redis_key_indexing_suf, 'actress'.lower()+':others')
    # print 'find: cast ', info, column_index
    x[x_row_index, column_index] = 1
    # print 'set: ', x_row_index, column_index
    # debug_x()


def set_numeric_column_value(key, info):
    global x_row_index
    global x
    column_index = (int)(r.hget(redis_key_indexing_pre + key + redis_key_indexing_suf, key))
    if key == 'year':
        x[x_row_index, column_index] = (float)(info-min_year) / (float)(max_year - min_year)
    if key == 'running time':
        x[x_row_index, column_index] = (float)(info-min_running_time) / (float)(max_running_time-min_running_time)

def test_matrix_form(nMovie):
    global x_row_index
    global test_id_matrix
    if nMovie.color != None:
        infos = nMovie.color.split(':')
        for info in infos:
            set_column_value('color', info)

    if nMovie.genre != None:
        infos = nMovie.genre.split(':')
        for info in infos:
            set_column_value('genre', info)

    if nMovie.language != None:
        infos = nMovie.language.split(':')
        for info in infos:
            set_column_value('language', info)

    if nMovie.soundmix != None:
        infos = nMovie.soundmix.split(':')
        for info in infos:
            set_column_value('soundmix', info)

    if nMovie.country != None:
        infos = nMovie.country.split(':')
        for info in infos:
            set_column_value('country', info)

    if nMovie.cast != None:
        infos = nMovie.cast.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_cast_column_value(_info)

    if nMovie.producer != None:
        infos = nMovie.producer.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('producer', _info)

    if nMovie.writer != None:
        infos = nMovie.writer.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('writer', _info)

    if nMovie.cinematographer != None:
        infos = nMovie.cinematographer.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('cinematographer', _info)

    if nMovie.composer != None:
        infos = nMovie.composer.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('composer', _info)

    if nMovie.costume_designer != None:
        infos = nMovie.costume_designer.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('costume designer', _info)

    if nMovie.director != None:
        infos = nMovie.director.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('director', _info)

    if nMovie.editor != None:
        infos = nMovie.editor.split(':')
        for info in infos:
            space_index = info.rfind(' ')
            left = info[space_index+1:]
            right = info[0:space_index]
            _info = left + ', ' + right
            set_column_value('editor', _info)

    if nMovie.company != None:
        infos = nMovie.company.split(':')
        for info in infos[:-1]:
            set_column_value('company', info)

    set_numeric_column_value('running time', nMovie.running_time)
    set_numeric_column_value('year', nMovie.year)

    test_id_matrix[x_row_index, 0] = nMovie.id

    x_row_index += 1


def test_matrix():
    test_matrix_init()
    test_cur = conn.cursor()

    count = test_cur.execute('SELECT * FROM new_movies')
    print "test_set's ", " size: ", count
    nMovie = None
    for i in range(count):
        nMovie = newMovie()
        result = test_cur.fetchone()
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
        print 'handing %sth: %s' % (i, nMovie.id)
        test_matrix_form(nMovie)

    test_cur.close()
    np.savetxt('testFeature.txt', x)
    np.savetxt('testId.txt', test_id_matrix)


def run():
    test_matrix()
    conn.close()
    print 'test_matrix done.'

if __name__ == '__main__':
    run()
