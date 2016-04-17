#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import MySQLdb
import numpy as np

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '1227401054'
mysql_db = 'mrp'
conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset="utf8")

redis_ip = 'localhost'
redis_port = 6379
redis_key_indexing_pre = 'mrp:'
redis_key_indexing_suf = ':indexing'
redis_key_counting_suf = ':counting'
r = redis.Redis(host=redis_ip, port=redis_port)

m = 0
d = 0
k = 10
x = None
y = None
x_row_index = 0
y_row_index = 0

begin_year = 2011
end_year = 2015

max_year = 2017
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

info_type_ids = {
    'color': 2,
    'genre': 3,
    'language': 4,
    'soundmix': 6,
    'country': 8,
}

role_type_ids = {
    'actor': 1,
    'actress': 2,
    'producer': 3,
    'writer': 4,
    'cinematographer': 5,
    'composer': 6,
    'costume designer': 7,
    'director': 8,
    'editor': 9,
}


def x_y_matrix_init():
    cur = conn.cursor()
    global x
    global y
    global m
    global d
    d=0
    for f in features:
        f_keys = r.hkeys(redis_key_indexing_pre+f+redis_key_indexing_suf)
        d += len(f_keys)
    for year in xrange(begin_year, end_year+1):
        count = cur.execute('SELECT count(*) FROM votes_dis WHERE year=%s', (year,))
        for i in xrange(count):
            m += cur.fetchone()[0]
    x = np.zeros((m, d), dtype=np.double)
    y = np.zeros((m, k), dtype=np.double)
    print "trainFeature's size: ", x.shape, "\ntrainDistribution's size: ", y.shape
    cur.close()


def x_matrix(movie_id, movie_year):
    cur = conn.cursor()
    global x_row_index
    global max_year
    global min_year
    global max_running_time
    global min_running_time
    column_index = None
    for key in info_type_ids.keys():
        count = cur.execute('SELECT info FROM movie_info WHERE info_type_id=%s AND movie_id=%s', (info_type_ids[key], movie_id))
        infos = []
        for i in xrange(count):
            result = cur.fetchone()
            infos.append(result[0])
        for info in infos:
            if r.hexists(redis_key_indexing_pre + key + redis_key_indexing_suf, info.lower()):
                column_index = r.hget(redis_key_indexing_pre + key + redis_key_indexing_suf, info.lower())
            else:
                column_index = r.hget(redis_key_indexing_pre + key + redis_key_indexing_suf, key.lower()+':others')
            x[x_row_index, column_index] = 1

    for key in role_type_ids.keys():
        count = cur.execute('SELECT person_id FROM cast_info WHERE movie_id=%s AND role_id=%s', (movie_id, role_type_ids[key]))
        person_ids = []
        for i in xrange(count):
            result = cur.fetchone()
            person_ids.append(result[0])
        for person_id in person_ids:
            person_count = cur.execute('SELECT name FROM name WHERE id=%s', (person_id, ))
            # person_count = 1
            name = cur.fetchone()[0]
            if r.hexists(redis_key_indexing_pre + key + redis_key_indexing_suf, name.lower()):
                column_index = r.hget(redis_key_indexing_pre + key + redis_key_indexing_suf, name.lower())
            else:
                column_index = r.hget(redis_key_indexing_pre+key+redis_key_indexing_suf, key+':others')
            x[x_row_index, column_index] = 1

    count = cur.execute('SELECT company_id FROM movie_companies WHERE movie_id=%s', (movie_id,))
    company_ids = []
    for i in xrange(count):
        result = cur.fetchone()
        company_ids.append(result[0])
    for company_id in company_ids:
        company_count = cur.execute('SELECT name FROM mrp.company_name WHERE id=%s', (company_id,))
        name = cur.fetchone()[0]
        if r.hexists(redis_key_indexing_pre + 'company' + redis_key_indexing_suf, name.lower()):
            column_index = r.hget(redis_key_indexing_pre + 'company' + redis_key_indexing_suf, name.lower())
        else:
            column_index = r.hget(redis_key_indexing_pre + 'company' + redis_key_indexing_suf, 'company'+':others')
        x[x_row_index, column_index] = 1

    column_index = r.hget(redis_key_indexing_pre + 'year' + redis_key_indexing_suf, 'year')
    x[x_row_index, column_index] = movie_year
    if movie_year > max_year:
        max_year=movie_year
    if movie_year < min_year:
        min_year = movie_year
    count = cur.execute('SELECT info FROM movie_info WHERE movie_id=%s AND info_type_id=%s', (movie_id, 1))
    if count == 0:
        running_time = '0'
    else:
        running_time = cur.fetchone()[0]
    if ':' in running_time:
        running_time = running_time[running_time.find(':')+1:]
    running_time = (int)(running_time)
    column_index = r.hget(redis_key_indexing_pre + 'running time' + redis_key_indexing_suf, 'running time')
    x[x_row_index, column_index] = running_time
    if running_time > max_running_time:
        max_running_time = running_time
    if running_time < min_running_time:
        min_running_time = running_time
    x_row_index += 1
    cur.close()


def process_x_numeric_value():
    global max_year
    global min_year
    global max_running_time
    global min_running_time
    global x
    print 'process numeric value.'
    print 'max_year:', max_year, ' min_year:', min_year
    print 'max_running_time:', max_running_time, ' min_running_time:', min_running_time
    r.set('mrp:max_year', max_year)
    r.set('mrp:min_year', min_year)
    r.set('mrp:max_running_time', max_running_time)
    r.set('mrp:min_running_time', min_running_time)
    print 'write max_min scale to redis.'
    year_column = (int)(r.hget(redis_key_indexing_pre + 'year' + redis_key_indexing_suf, 'year'))
    running_time_column = (int)(r.hget(redis_key_indexing_pre + 'running time' + redis_key_indexing_suf, 'running time'))
    for row in x:
        row[year_column] = (float)(row[year_column]-min_year) / (float)(max_year-min_year)
        row[running_time_column] = (float)(row[running_time_column]-min_running_time) / (float)(max_running_time-min_running_time)


def y_matrix(movie_id, movie_year):
    cur = conn.cursor()
    global y_row_index
    count = cur.execute('SELECT votes,votes_one,votes_two,votes_three,votes_four,votes_five,votes_six,votes_seven,votes_eight,votes_nine,votes_ten FROM votes_dis WHERE id=%s', (movie_id,))
    result = cur.fetchone()
    votes = result[0]
    y[y_row_index, 0] = result[1]*1.0 / votes
    y[y_row_index, 1] = result[2]*1.0 / votes
    y[y_row_index, 2] = result[3]*1.0 / votes
    y[y_row_index, 3] = result[4]*1.0 / votes
    y[y_row_index, 4] = result[5]*1.0 / votes
    y[y_row_index, 5] = result[6]*1.0 / votes
    y[y_row_index, 6] = result[7]*1.0 / votes
    y[y_row_index, 7] = result[8]*1.0 / votes
    y[y_row_index, 8] = result[9]*1.0 / votes
    y[y_row_index, 9] = result[10]*1.0 / votes
    y_row_index = y_row_index+1
    cur.close()


def x_y_matrix():
    x_y_matrix_init()
    cur_x_y = conn.cursor()

    for year in xrange(begin_year, end_year+1):
        count = cur_x_y.execute('SELECT id, year FROM votes_dis WHERE year=%s', (year,))
        print year, " traing_set's ", " size: ", count
        for i in xrange(count):
            result = cur_x_y.fetchone()
            movie_id = result[0]
            movie_year = result[1]
            print 'handing %sth, id:%s, year:%s' % (i, movie_id, movie_year)
            x_matrix(movie_id, movie_year)
            y_matrix(movie_id, movie_year)

    process_x_numeric_value()
    cur_x_y.close()

    # x: trainFeature
    # y: trainDistribution
    np.savetxt('features.txt', x)
    np.savetxt('distributions.txt', y)


def run():
    x_y_matrix()
    conn.close()
    print 'x_y_matrix done.'


if __name__ == '__main__':
    run()
