#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from Queue import Queue, Empty
except:
    from queue import Queue, Empty
import subprocess
import os
import imdb
import MySQLdb
from threading import Thread
from entity import oldMovie, votesMovie
import time

location = './dbfiles'
imdb_script = './code/bin/imdbpy2sql.py'
base_download_url = 'ftp://ftp.fu-berlin.de/pub/misc/movies/database/'
to_download_files = [
    'genres.list.gz', 'color-info.list.gz', 'directors.list.gz', 
    'actors.list.gz', 'actresses.list.gz', 'complete-cast.list.gz',
    'countries.list.gz', 'language.list.gz', 'writers.list.gz', 
    'editors.list.gz', 'cinematographers.list.gz', 'costume-designers.list.gz', 
    'composers.list.gz', 
    'sound-mix.list.gz', 'soundtracks.list.gz', 'production-companies.list.gz', 
    'running-times.list.gz', 'business.list.gz', 'crazy-credits.list.gz', 
    'movie-links.list.gz', 'keywords.list.gz', 
    'movies.list.gz', 'producers.list.gz', 'ratings.list.gz', 
    ]

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '1227401054'
mysql_db = 'mrp'

begin_year = 2011
end_year = 2011
old_movies_years = Queue(maxsize = 25)
old_movies_titles = Queue(maxsize = 450000)
old_movies_entites = Queue(maxsize = 400000)

'''
下载IMDB数据库镜像文件
'''
def download_db_files():
    for file in to_download_files:
        url = base_download_url + file
        print 'Downloading ', url
        args = ['wget', '-P', location, url]
        t_pro = subprocess.Popen(args)
        # block model too slow
        #t_pro.wait()

'''
通过IMDBPY脚本，将数据库镜像转为本地数据库
'''
def trans_db_to_local():
    while True:
        allDone = True
        for file in to_download_files:
            if not os.path.isfile(location + '/' + file):
                #print 'need file: ', location+file
                allDone = False
                break
        if allDone == True:
            break

    print 'Running imdbpy2sql.py begin'
    # mysql://user:password@host/database
    mysql_list = ['mysql://', mysql_user, ':', mysql_passwd, '@', mysql_ip, '/', mysql_db]
    subprocess.call(imdb_script + ' -d ' + location + ' -u ' + ''.join(mysql_list) + ' --mysql-force-myisam', shell=True)
    print 'Running imdbpy2sql.py. over'


def year_thread():
    for year in xrange(begin_year, end_year+1):
        # print year
        old_movies_years.put(year)


def title_thread():
    conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset="utf8")
    cur = conn.cursor()
    while True:
        try:
            year = old_movies_years.get()
            count = cur.execute('SELECT id, title FROM title WHERE kind_id=%s AND production_year=%s LIMIT 0, 1000', (1, year))
            for i in xrange(count):
                result = cur.fetchone()
                _oldMovie = oldMovie()
                _oldMovie.id = result[0]
                _oldMovie.title = result[1]
                _oldMovie.year = year
                old_movies_titles.put(_oldMovie)
            old_movies_years.task_done()
        except Exception as e:
            print 'title_thread: An {} exception occured.'.format(e)
    conn.close()


def entities_thread():
    ia = imdb.IMDb()
    while True:
        _oldMovie = None
        try:
            _oldMovie = old_movies_titles.get()
            s_result = ia.search_movie(_oldMovie.title)
            # the_unt = s_result[0]
            for the_unt in s_result:
                if the_unt['title'] != _oldMovie.title:
                    continue

                if the_unt.has_key('year'):
                    if the_unt['year'] != _oldMovie.year:
                        continue
                
                ia.update(the_unt, info=('vote details'))

                if the_unt.has_key('votes'):
                    if the_unt['votes'] < 5:
                        continue
                else:
                    continue

                _votesMovie = votesMovie()

                _votesMovie.id = _oldMovie.id
                _votesMovie.title = _oldMovie.title
                _votesMovie.year = _oldMovie.year

                if the_unt.has_key('rating'):
                    _votesMovie.rating = the_unt['rating']
                if the_unt.has_key('votes'):
                    _votesMovie.votes = the_unt['votes']
                if the_unt.has_key('number of votes'):
                    number_votes = the_unt['number of votes']
                    _votesMovie.votes_one = number_votes[1]
                    _votesMovie.votes_two = number_votes[2]
                    _votesMovie.votes_three = number_votes[3]
                    _votesMovie.votes_four = number_votes[4]
                    _votesMovie.votes_five = number_votes[5]
                    _votesMovie.votes_six = number_votes[6]
                    _votesMovie.votes_seven = number_votes[7]
                    _votesMovie.votes_eight = number_votes[8]
                    _votesMovie.votes_nine = number_votes[9]
                    _votesMovie.votes_ten = number_votes[10]
                if the_unt.has_key('demographic'):
                    demo_value = the_unt['demographic']
                    (_votesMovie.votes_males, _votesMovie.rating_males) = (demo_value.get('males')[0], demo_value.get('males')[1]) if demo_value.get('males')!=None else (0, 0.0)
                    (_votesMovie.votes_females, _votesMovie.rating_females) = (demo_value.get('females')[0], demo_value.get('females')[1]) if demo_value.get('females')!=None else (0, 0.0)
                    (_votesMovie.votes_aged_under_eighteen, _votesMovie.rating_aged_under_eighteen) = (demo_value.get('aged under 18')[0], demo_value.get('aged under 18')[1]) if demo_value.get('aged under 18')!=None else (0, 0.0)
                    (_votesMovie.votes_males_under_eighteen, _votesMovie.rating_males_under_eighteen) = (demo_value.get('males under 18')[0], demo_value.get('males under 18')[1]) if demo_value.get('males under 18')!=None else (0, 0.0)
                    (_votesMovie.votes_females_under_eighteen, _votesMovie.rating_females_under_eighteen) = (demo_value.get('females under 18')[0], demo_value.get('females under 18')[1]) if demo_value.get('females under 18')!=None else (0, 0.0)
                    (_votesMovie.votes_aged_eighteen_twentyNine, _votesMovie.rating_aged_eighteen_twentyNine) = (demo_value.get('aged 18-29')[0], demo_value.get('aged 18-29')[1]) if demo_value.get('aged 18-29')!=None else (0 ,0.0)
                    (_votesMovie.votes_males_eighteen_twentyNine, _votesMovie.rating_males_eighteen_twentyNine) = (demo_value.get('males aged 18-29')[0], demo_value.get('males aged 18-29')[1]) if demo_value.get('males aged 18-29')!=None else (0, 0.0)
                    (_votesMovie.votes_females_eighteen_twentyNine, _votesMovie.rating_females_eighteen_twentyNine) = (demo_value.get('females aged 18-29')[0], demo_value.get('females aged 18-29')[1]) if demo_value.get('females aged 18-29')!=None else (0, 0.0)
                    (_votesMovie.votes_aged_thirty_fourtyFour, _votesMovie.rating_aged_thirty_fourtyFour) = (demo_value.get('aged 30-44')[0], demo_value.get('aged 30-44')[1]) if demo_value.get('aged 30-44')!=None else (0, 0.0)
                    (_votesMovie.votes_males_thirty_fourtyFour, _votesMovie.rating_males_thirty_fourtyFour) = (demo_value.get('males aged 30-44')[0], demo_value.get('males aged 30-44')[1]) if demo_value.get('males aged 30-44')!=None else (0, 0.0)
                    (_votesMovie.votes_females_thirty_fourtyFour, _votesMovie.rating_females_thirty_fourtyFour) = (demo_value.get('females aged 30-44')[0], demo_value.get('females aged 30-44')[1]) if demo_value.get('females aged 30-44')!=None else (0, 0.0)
                    (_votesMovie.votes_aged_fourtyFive, _votesMovie.rating_aged_fourtyFive) = (demo_value.get('aged 45+')[0], demo_value.get('aged 45+')[1]) if demo_value.get('aged 45+')!=None else (0, 0.0)
                    (_votesMovie.votes_males_fourtyFive, _votesMovie.rating_males_fourtyFive) = (demo_value.get('males aged 45+')[0], demo_value.get('males aged 45+')[1]) if demo_value.get('males aged 45+')!=None else (0, 0.0)
                    (_votesMovie.votes_females_fourtyFive, _votesMovie.rating_females_fourtyFive) = (demo_value.get('females aged 45+')[0], demo_value.get('females aged 45+')[1]) if demo_value.get('females aged 45+')!=None else (0, 0.0)
                    (_votesMovie.votes_imdb_staff, _votesMovie.rating_imdb_staff) = (demo_value.get('imdb staff')[0], demo_value.get('imdb staff')[1]) if demo_value.get('imdb staff')!=None else (0, 0.0)
                    (_votesMovie.votes_top_thousand_voters, _votesMovie.rating_top_thousand_voters) = (demo_value.get('top 1000 voters')[0], demo_value.get('top 1000 voters')[1]) if demo_value.get('top 1000 voters')!=None else (0, 0.0)
                    (_votesMovie.votes_us_users, _votesMovie.rating_us_users) = (demo_value.get('us users')[0], demo_value.get('us users')[1]) if demo_value.get('us users')!=None else (0, 0.0)
                    (_votesMovie.votes_nous_users, _votesMovie.rating_nous_users) = (demo_value.get('non-us users')[0], demo_value.get('non-us users')[1]) if demo_value.get('non-us users')!=None else (0, 0.0)
                old_movies_entites.put(_votesMovie)
                old_movies_titles.task_done()
            time.sleep(0.5)
        except Exception as e:
            old_movies_titles.put(_oldMovie)
            print 'entities_thread: An {} exception occured.'.format(e)
            

def db_thread():
    conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset="utf8")
    cur = conn.cursor()
    while True:
        old_movie = None
        try:
            old_movie = old_movies_entites.get()
            cur.execute("INSERT INTO votes_dis values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (old_movie.id, old_movie.title, old_movie.year, old_movie.rating, old_movie.votes,
                            old_movie.votes_one, old_movie.votes_two, old_movie.votes_three, old_movie.votes_four, old_movie.votes_five,
                            old_movie.votes_six, old_movie.votes_seven, old_movie.votes_eight, old_movie.votes_nine, old_movie.votes_ten,
                            old_movie.votes_males, old_movie.rating_males, old_movie.votes_females, old_movie.rating_females,
                            old_movie.votes_aged_under_eighteen, old_movie.rating_aged_under_eighteen,
                            old_movie.votes_males_under_eighteen, old_movie.rating_males_under_eighteen,
                            old_movie.votes_females_under_eighteen, old_movie.rating_females_under_eighteen,
                            old_movie.votes_aged_eighteen_twentyNine, old_movie.rating_aged_eighteen_twentyNine,
                            old_movie.votes_males_eighteen_twentyNine, old_movie.rating_males_eighteen_twentyNine,
                            old_movie.votes_females_eighteen_twentyNine, old_movie.rating_females_eighteen_twentyNine,
                            old_movie.votes_aged_thirty_fourtyFour, old_movie.rating_aged_thirty_fourtyFour,
                            old_movie.votes_males_thirty_fourtyFour, old_movie.rating_males_thirty_fourtyFour,
                            old_movie.votes_females_thirty_fourtyFour, old_movie.rating_females_thirty_fourtyFour,
                            old_movie.votes_aged_fourtyFive, old_movie.rating_aged_fourtyFive,
                            old_movie.votes_males_fourtyFive, old_movie.rating_males_fourtyFive,
                            old_movie.votes_females_fourtyFive, old_movie.rating_females_fourtyFive,
                            old_movie.votes_imdb_staff, old_movie.rating_imdb_staff,
                            old_movie.votes_top_thousand_voters, old_movie.rating_top_thousand_voters,
                            old_movie.votes_us_users, old_movie.rating_us_users,
                            old_movie.votes_nous_users, old_movie.rating_nous_users
                            )
                        )
            conn.commit()
            print 'insert: %s, %s' % (old_movie.id, old_movie.title)
            old_movies_entites.task_done()
        except Exception as e:
            print 'db_thread: An {} exception occured.'.format(e)
    conn.close()


def run():
    # download_db_files()
    # trans_db_to_local()
    year_t = Thread(target = year_thread)
    title_t = Thread(target = title_thread)
    for i in range(3):
        entities_t = Thread(target = entities_thread)
        entities_t.start()
    db_t = Thread(target = db_thread)
    year_t.start()
    title_t.start()
    db_t.start()
    old_movies_years.join()
    old_movies_titles.join()
    old_movies_entites.join()

if __name__ == '__main__':
    run()
