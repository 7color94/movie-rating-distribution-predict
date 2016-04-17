#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import MySQLdb
from entity import oldMovie

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '1227401054'
mysql_db = 'mrp'
conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset="utf8")
cur = conn.cursor()

redis_ip = 'localhost'
redis_port = 6379
redis_key_counting_pre = 'mrp:'
redis_key_counting_suf = ':counting'
r = redis.Redis(host=redis_ip, port=redis_port)

begin_year = 2012
end_year = 2015

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


def training_set(year):
    oldMovies = []
    count = cur.execute('SELECT id, title FROM votes_dis WHERE year=%s', (year,))
    print year, ': ', count
    for i in xrange(count):
        result = cur.fetchone()
        _oldMovie = oldMovie()
        _oldMovie.id = result[0]
        _oldMovie.title = result[1]
        _oldMovie.year = year
        oldMovies.append(_oldMovie)
    print "size of training_set in %s is: %s" % (year, len(oldMovies))
    return oldMovies


def features_counting():
    for year in xrange(begin_year, end_year+1):
        oldMovies = training_set(year)
        pipe = r.pipeline(False)
        _i = -1
        for _oldMovie in oldMovies:
            _i += 1
            movie_id = _oldMovie.id
            print 'handling ', _i, 'th, movie_id: ', movie_id
            '''
            info_type_ids = {
                'color': 2,
                'genre': 3,
                'language': 4,
                'soundmix': 6,
                'country': 8,
            }
            '''
            for key in info_type_ids.keys():
                count = cur.execute('SELECT info FROM movie_info WHERE info_type_id=%s AND movie_id=%s', (info_type_ids[key], movie_id))
                infos = []
                for i in xrange(count):
                    result = cur.fetchone()
                    infos.append(result[0])
                for info in infos:
                    pipe.zincrby(redis_key_counting_pre+key+redis_key_counting_suf, info.lower(), 1)

            '''
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
            '''
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
                    pipe.zincrby(redis_key_counting_pre+key+redis_key_counting_suf, name.lower(), 1)
            
            '''
            company
            '''
            count = cur.execute('SELECT company_id FROM movie_companies WHERE movie_id=%s', (movie_id, ))
            company_ids = []
            for i in xrange(count):
                result = cur.fetchone()
                company_ids.append(result[0])
            for company_id in company_ids:
                company_count = cur.execute('SELECT name FROM mrp.company_name WHERE id=%s', (company_id, ))
                name = cur.fetchone()[0]
                pipe.zincrby(redis_key_counting_pre+'company'+redis_key_counting_suf, name.lower(), 1)

            pipe.execute()


def run():
    features_counting()
    cur.close()
    conn.close()
    print 'features_counting done.'
    

if __name__ == '__main__':
    run()