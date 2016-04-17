from __future__ import division
import threading
import os
from imdb import IMDb
import xml.etree.ElementTree as ET

ib = IMDb()

def initMovieItems():
    items = []
    items.append("title")
    items.append("year")
    items.append("genres")
    items.append("director")
    items.append("producer")
    items.append("writer")
    items.append("editor")
    items.append("cast")
    items.append("original music")
    items.append("production companies")
    items.append("distributors")
    items.append("runtimes")
    items.append("countries")
    items.append("languages")

    return items

def getMovieByTitleAndYear(title, year):
    movies = ib.search_movie(title)
    id = ""
    for mv in movies:
        if str(mv['year']) == year:
            ib.update(mv)
            return mv
        
    return None

def getMovieByIMDBId(id):
    movie = ib.get_movie(id)
    if not movie:
        return None
    
    items = initMovieItems()
    data = ""
    for item in items:
        content = movie.get(item)
        if not content:
            data = data + "  "
        else:
            if isinstance(content, list):
                for i in range(len(content)):
                    data = data + str(content[i]) + "|"
                data = data[:-1]
            else:
                data = data + str(content)
        data = data + "::"
    data = data[:-2]
    
    return data

def IMDBParser(mapfile, outfile):
    fin = open(mapfile, 'r')
    fout = open(outfile, 'w+')
    
    for count, line in enumerate(fin):
        print count
        #if count % 10 == 0:
        #   print count
        
        data = line.split(",")
        nxid = data[0]
        ibid = data[1].split("/")[-2].replace("tt", "")
        
        content = getMovieByIMDBId(ibid)
        if content is None:
            continue
        line = nxid + "::" + content + "\n"
        fout.write(line)
        
    fin.close()
    fout.close()
    
def CountNetflixRating():
    basepath = "F:\\Research\\Dataset\\NetflixPrize\\training_set\\"
    fout = open(basepath + "rating.txt", 'w+')
    
    for i in range(1, 17771):
        fname = basepath + "mv_" + str(i).zfill(7) + ".txt"
        file = open(fname, 'r')
        if not file:
            continue
        
        rates = [0,0,0,0,0]
        for line in file:
            data = line.split(",")
            if len(data) > 2:
                rate = int(line.split(",")[1]) - 1
                rates[rate] = rates[rate] + 1
        rating = str(i) + ","
        _sum = sum(rates)
        for i in range(len(rates)): 
            rating = rating + str(round(rates[i] / _sum, 2)) + ","
        rating = rating[:-1] + "\n"
        fout.write(rating)
    
    fout.close() 
    
def CrawelMovieAsXML(mapfile, outdir):
    fin = open(mapfile, 'r')
    
    for count, line in enumerate(fin):
        print count
        #if count % 10 == 0:
        #   print count
        
        data = line.split(",")
        nxid = data[0]
        ibid = data[1].split("/")[-2].replace("tt", "")
        movie = ib.get_movie(ibid)
        if not movie:
            continue
        ib.update(movie, 'business')
        
        fout = open(outdir + nxid + ".txt", 'w+')
        fout.write(movie.asXML())
        fout.close()
        
    fin.close()
        
def ParseXMLFile(root):
    line = ""
    
    # title
    line += root.find('title').text + "::"
    
    # year
    year = root.find('year')
    if year is None or year.text == '':
        line += "None::"
    else:
        line += year.text + "::"
    
    # genres
    ele = root.find('genres')
    if ele is None or len(ele)==0:
        line += "None::"
    else:
        for text in ele.itertext():
            line += text + "|"
        line = line[:-1] + "::"
    
    # roles
    roles = ['director', 'writer', 'editor','cinematographer', 'art-direction', 
             'costume-designer', 'original-music'] 
    for role in roles:
        ele = root.find(role)
        if ele is None or len(ele)==0:
            line += "None::"
        else:
            line += ele.find('person').attrib.get('id') + "::"
    
    # production company
    ele = root.find('production-companies')
    if ele is None or len(ele)==0:
        line += "None::"
    else:
        line += ele.find('company').attrib.get('id') + "::"
        
    # actor
    cast = root.find('cast')
    if cast is None or len(cast) == 0:
        line += "None::None::None::"
    else:
        cast = cast.findall('person')
        for i in range(3):
            if i < len(cast):
                line += cast[i].attrib.get('id') + "::"
            else:
                line += "None::"
            
    # country, language, color, sound, run time
    parts = ['country-codes', 'language-codes', 'color-info', 'sound-mix', 'runtimes']
    for part in parts:
        ele = root.find(part)
        if ele is None or len(ele)==0 or ele[0].text=='':
            line += "None::"
        else:
            line += ele[0].text + "::"
    
    # budget and gross
    parts = ['budget', 'gross']
    business = root.find('business')
    if business is None or len(business)==0:
        line += "None::None::"
    else:
        for part in parts:
            ele = business.find(part)
            if ele is None or len(ele)==0 or ele[0].text=='':
                line += "None::"
            else:
                line += ele[0].text + "::"
    
    line = line.encode('UTF-8')
    return line
    
        
def ParseXMLFiles(basepath):
    fout = open(basepath+"\\movies.txt", 'w+')
    list_dirs = os.walk(basepath)
    for root, dirs, files in list_dirs:
        for f in files:
            id = f.split('.')[0]
            print id
            r = ET.ElementTree(file=os.path.join(root,f)).getroot()
            line = ParseXMLFile(r)
            fout.write(str(id) + "::" + line + "\n")
    fout.close()
    
if __name__ == '__main__':
    
    basepath = "E:\\Dataset\\NetflixPrize\\movies"
    '''threads = []
    for i in range(1,6):
        inpath = basepath + "mapping" + str(i) + ".txt"
        outpath = basepath + "movies" + str(i) + ".txt"
        try:
            t = threading.Thread(target=IMDBParser, args=(inpath, outpath))
            threads.append(t)
            t.start()
        except:
            print "error " + str(i)
    '''
    
    '''
    inpath = basepath + "mapping1.txt"
    outpath = basepath + "movie_content1.txt"
    IMDBParser(inpath, outpath)
    '''
    #CountNetflixRating()
    
    '''
    threads = []
    for i in range(1,6):
        inpath = basepath + "mapping" + str(i) + ".txt"
        outpath = basepath + "movies\\"
        try:
            t = threading.Thread(target=CrawelMovieAsXML, args=(inpath, outpath))
            threads.append(t)
            t.start()
        except:
            print "error " + str(i)
    '''
    #CrawelMovieAsXML(basepath+"mapping.txt", basepath+"XML\\")
    ParseXMLFiles(basepath + "\\XML")