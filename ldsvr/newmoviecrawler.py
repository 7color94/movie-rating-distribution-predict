#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from Queue import Queue, Empty
except:
    from queue import Queue, Empty
from threading import Thread
import requests
from bs4 import BeautifulSoup
import re
from entity import newMovie
import MySQLdb

year = 2016
begin_month = 1
end_month = 12
imdb_base_url = 'http://www.imdb.com'

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '1227401054'
mysql_db = 'mrp'

index_url = Queue(maxsize = 12)
movie_url = Queue(maxsize = 500)
entities = Queue(maxsize = 500)


def index_thread():
    base_url = imdb_base_url + '/movies-coming-soon/'
    for m in xrange(begin_month, end_month+1):
        try:
            date = '%d-%02d' % (year, m)
            #print date
            index_url.put(base_url + date)
        except Exception as e:
            print 'index_thread: An {} exception occured'.format(e)


def movie_thread():
    while True:
        try:
            url = index_url.get()
            #print url
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            list_item = soup.findAll(True, {'class': "list_item"})
            for item in list_item:
                h4 = item.findAll('h4')
                for h in h4:
                    #print h.find('a').get('href')
                    link = h.find('a').get('href')
                    link = link[0: link.index('?')-1]
                    movie_url.put(imdb_base_url + link)
                    #print imdb_base_url + link
            index_url.task_done()
        except Exception as e:
            print 'movie_thread: An {} exception occured'.format(e)


def detail_thread():
    while True:
        m_url = None
        try:
            m_url = movie_url.get()
            # print 'detail_thread fetch: ', m_url
            r = requests.get(m_url)
            soup = BeautifulSoup(r.content)
            nMovie = newMovie()
            
            # id
            nMovie.id = m_url[m_url.index('/tt')+3:]
            # imdb_url
            nMovie.imdb_url = m_url
            # year
            nMovie.year = year

            # poster_url
            poster = soup.find('div', {'class': 'poster'}).find('img')
            newMovie.poster_url = poster.get('src')
            # title
            nMovie.title = soup.find('div', {'class': 'title_bar_wrapper'}).find(attrs={'itemprop': 'name'}).text

            title_details = soup.find('div', {'id': 'titleDetails'})
            txt_block = title_details.findAll('div', {'class': 'txt-block'})
            for t in txt_block:
                try:
                    # countries
                    if t.find('h4').text == 'Country:':
                        c_links = t.findAll('a')
                        if len(c_links) > 0:
                            country = c_links[0].text
                            for c in c_links[1:]:
                                country = country + ':' + c.text
                            nMovie.country = country
                    # languages
                    if t.find('h4').text == 'Language:':
                        l_links = t.findAll('a')
                        if len(l_links) > 0:
                            lan = l_links[0].text
                            for l in l_links[1:]:
                                lan = lan + ':' + l.text
                            nMovie.language = lan
                    # production_companies
                    if t.find('h4').text.strip() == 'Production Co:':
                        p_c_links = t.findAll('a')
                        if len(p_c_links) > 0:
                            p_companies = p_c_links[0].text
                            for p_c in p_c_links[1:]:
                                p_companies = p_companies + ':' + p_c.text
                            nMovie.company = p_companies
                    # color
                    if t.find('h4').text == 'Color:':
                        color_links = t.findAll('a')
                        if len(color_links) > 0:
                            colors = color_links[0].text
                            for t_color in color_links[1:]:
                                colors = colors + ':' + t_color.text
                            nMovie.color = colors
                    # sound_mix
                    if t.find('h4').text == 'Sound Mix:':
                        sound_mix_links = t.findAll('a')
                        if len(sound_mix_links) > 0:
                            s_mxs = sound_mix_links[0].text
                            for s_m in sound_mix_links[1:]:
                                s_mxs = s_mxs + ':' + s_m.text
                            nMovie.soundmix = s_mxs
                    # running_time
                    if t.find('h4').text == 'Runtime:':
                        runtime_links = t.findAll('time', {'itemprop': 'duration'})
                        if len(runtime_links) > 0:
                            r_t = runtime_links[0].text.strip().split(' ')[0]
                            nMovie.running_time = r_t
                except:
                    continue
                    #print 'detail_thread: txt_block find no h4 tag'

            # keywords
            keywords = soup.findAll(attrs={'itemprop': 'keywords', 'class': 'itemprop'})
            #print m_url, ' keywords:', len(keywords)
            if len(keywords) > 0:
                key_words = keywords[0].text
                for k in keywords[1:]:
                    key_words = key_words + ':' + k.text
                nMovie.keywords = key_words

            # genres
            genres_div = soup.find(attrs={'class': 'see-more inline canwrap', 'itemprop': 'genre'})
            if genres_div != None:
                g_links = genres_div.findAll('a')
                #print m_url, ' genres:', len(g_links)
                if len(g_links) > 0:
                    genres = g_links[0].text.strip()
                    for g in g_links[1:]:
                        genres = genres + ':' + g.text.strip()
                    #print genres
                    nMovie.genre = genres

            # cast
            cast_td = soup.findAll(attrs={'itemprop': 'actor'})
            #print m_url, ' cast:', len(cast_td)
            if len(cast_td) > 0:
                casts = cast_td[0].find(attrs={'class': 'itemprop', 'itemprop': 'name'}).text
                for c in cast_td[1:]:
                    casts = casts + ':' + c.find(attrs={'class': 'itemprop', 'itemprop': 'name'}).text
                #print casts
                nMovie.cast = casts
            
            full_cast_url = m_url + '/fullcredits'
            full_cast_r = requests.get(full_cast_url)
            full_cast_soup = BeautifulSoup(full_cast_r.content)
            data_headers = full_cast_soup.findAll('h4', {'class': 'dataHeaderWithBorder'})
            credits_tables = full_cast_soup.findAll('table', {'class': 'simpleTable simpleCreditsTable'})
            # print len(data_headers), ' ', len(credits_tables)
            for i in range(len(data_headers)):
                # print i, ' :', data_headers[i].text, len(data_headers[i].text)
                # director
                if data_headers[i].text.strip() == 'Directed by':
                    table_data = credits_tables[i]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    directors = td_name[0].find('a').text.strip()
                    for d_name in td_name[1:]:
                        directors = directors + ':' + d_name.find('a').text.strip()
                    newMovie.director = directors
                # writer
                if data_headers[i].text.strip() == 'Writing Credits':
                    table_data = credits_tables[i]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    writers = td_name[0].find('a').text.strip()
                    for w_name in td_name[1:]:
                        writers = writers + ':' + w_name.find('a').text.strip()
                    newMovie.writer = writers
                # producer
                if data_headers[i].text.strip() == 'Produced by':
                    table_data = credits_tables[i-1]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    producers = td_name[0].find('a').text.strip()
                    for p_name in td_name[1:]:
                        producers = producers + ':' + p_name.find('a').text.strip()
                    newMovie.producer = producers
                # Cinematography by 
                if data_headers[i].text.strip() == 'Cinematography by':
                    table_data = credits_tables[i-1]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    cinematographys = td_name[0].find('a').text.strip()
                    for _name in td_name[1:]:
                        cinematographys = cinematographys + ':' + _name.find('a').text.strip()
                    newMovie.cinematographer = cinematographys
                # composer:Music by 
                if data_headers[i].text.strip() == 'Music by':
                    table_data = credits_tables[i-1]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    composers = td_name[0].find('a').text.strip()
                    for _name in td_name[1:]:
                        composers = composers + ':' + _name.find('a').text.strip()
                    newMovie.composer = composers
                # Costume Design by  
                if data_headers[i].text.strip() == 'Costume Design by':
                    table_data = credits_tables[i-1]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    costumes = td_name[0].find('a').text.strip()
                    for _name in td_name[1:]:
                        costumes = costumes + ':' + _name.find('a').text.strip()
                    newMovie.costume_designer = costumes
                # editor:Editorial Department 
                if data_headers[i].text.strip() == 'Editorial Department':
                    table_data = credits_tables[i-1]
                    td_name = table_data.findAll('td', {'class': 'name'})
                    editors = td_name[0].find('a').text.strip()
                    for _name in td_name[1:]:
                        editors = editors + ':' + _name.find('a').text.strip()
                    newMovie.editor = editors
            entities.put(nMovie)
            movie_url.task_done()
        except Exception as e:
            movie_url.put(m_url)
            print 'detail_thread: An {} exception occured'.format(e)


def db_thread():
    conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
    cur = conn.cursor()
    while True:
        try:
            nMovie = entities.get()
            cur.execute("INSERT INTO new_movies values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (nMovie.id, nMovie.title, nMovie.color,
                        nMovie.genre, nMovie.language, nMovie.soundmix,
                        nMovie.country, nMovie.cast, nMovie.producer,
                        nMovie.writer, nMovie.cinematographer, nMovie.composer,
                        nMovie.costume_designer, nMovie.director, nMovie.editor,
                        nMovie.company, nMovie.year, nMovie.running_time,
                        nMovie.keywords, nMovie.imdb_url, nMovie.poster_url,
                        ))
            conn.commit()
            print 'insert %s, %s success.' % (nMovie.id, nMovie.title)
            entities.task_done()
        except Exception as e:
            print 'db_thread: An {} exception occured'.format(e)
    conn.close()


def run():
    print 'new movie crawl task begin'
    index_t = Thread(target = index_thread)
    movie_t = Thread(target = movie_thread)
    detail_t = Thread(target = detail_thread)
    db_t = Thread(target = db_thread)
    index_t.start()
    movie_t.start()
    detail_t.start()
    db_t.start()
    index_url.join()
    movie_url.join()
    entities.join()
    print 'new movie crawl task over'

if __name__ == '__main__':
    run()
