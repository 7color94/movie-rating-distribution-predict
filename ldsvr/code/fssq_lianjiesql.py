#-*- coding: UTF-8 -*-
import imdb
import MySQLdb
import os
import xlrd
import xlwt
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
ia=imdb.IMDb()
#s_result=ia.search_movie('The Untouchables')
#for item in s_result:
#    print item['long imdb canonical title'], item.movieID
#the_unt=s_result[0]
conn=MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    db='imdb',
)
cur=conn.cursor()
cou=conn.cursor()
#cur.execute("SELECT * FROM imdb.title where id=2337200;")
#cur.execute("SELECT * FROM imdb.title where production_year=2014 and kind_id=1 limit 29006,51270;")
cur.execute("SELECT * FROM imdb.title, imdb.movie_info_idx where production_year=1995 and kind_id=1 and info_type_id=101 and info!=0 and title.id=movie_info_idx.movie_id limit 2765,2910;")
#c=cou.fetchone()
#count=c[0]
#print count
start_time = list(time.localtime())


#创建EXCEL表格 初始化******************************************
book=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('data',cell_overwrite_ok=True)
sheet.write(0,0,'Title')
sheet.write(0,1,'Year')
sheet.write(0,2,'Countries')
sheet.write(0,3,'Languages')

sheet.write(0,4,'Keywords')
sheet.write(0,5,'Genres')
sheet.write(0,6,'Cast')
sheet.write(0,7,'Editor')
sheet.write(0,8,'Writer')


sheet.write(0,9,'Production companies')
sheet.write(0,10,'Director')
sheet.write(0,11,'Producer')
sheet.write(0,12,'Votes')
sheet.write(0,13,'Rating')

sheet.write(0,14,'R=1')
sheet.write(0,15,'R=2')
sheet.write(0,16,'R=3')
sheet.write(0,17,'R=4')
sheet.write(0,18,'R=5')
sheet.write(0,19,'R=6')
sheet.write(0,20,'R=7')
sheet.write(0,21,'R=8')
sheet.write(0,22,'R=9')
sheet.write(0,23,'R=10')



sheet.write(0,24,'Males')
sheet.write(0,25,'Males Rating')

sheet.write(0,26,'Females')
sheet.write(0,27,'Females Rating')

sheet.write(0,28,'Aged under 18')
sheet.write(0,29,'Aged under 18 Rating')

sheet.write(0,30,'Males under 18')
sheet.write(0,31,'Males under 18 Rating')

sheet.write(0,32,'Females under 18')
sheet.write(0,33,'Females under 18 Rating')

sheet.write(0,34,'Aged 18-29')
sheet.write(0,35,'Aged 18-29 Rating')

sheet.write(0,36,'Males Aged 18-29')
sheet.write(0,37,'Males Aged 18-29 Rating')

sheet.write(0,38,'Females Aged 18-29')
sheet.write(0,39,'Females Aged 18-29 Rating')

sheet.write(0,40,'Aged 30-44')
sheet.write(0,41,'Aged 30-44 Rating')

sheet.write(0,42,'Males Aged 30-44')
sheet.write(0,43,'Males Aged 30-44 Rating')

sheet.write(0,44,'Females Aged 30-44')
sheet.write(0,45,'Females Aged 30-44 Rating')

sheet.write(0,46,'Aged 45+')
sheet.write(0,47,'aged 45+ Rating')

sheet.write(0,48,'Males Aged 45+')
sheet.write(0,49,'Males Aged 45+ Rating')

sheet.write(0,50,'Females Aged 45+')
sheet.write(0,51,'Females Aged 45+ Rating')

sheet.write(0,52,'IMDb staff')
sheet.write(0,53,'IMDb staff Rating')

sheet.write(0,54,'Top 1000 voters')
sheet.write(0,55,'Top 1000 voters Rating')

sheet.write(0,56,'US users')
sheet.write(0,57,'US users Rating')

sheet.write(0,58,'Non-US users')
sheet.write(0,59,'Non-US users Rating')

sheet.write(0,60,'ID')
# sheet.write(0,0,'Title')
# sheet.write(0,1,'Votes')
# sheet.write(0,2,'Rating')
# sheet.write(0,3,'R1')
# sheet.write(0,4,'aged 45+')
# sheet.write(0,5,'aged 45+ R')
#*************************************************************


#for i in range(1,count+1):
#while title!=None
i=0
kk=1
year=1995
for number in range(1,6000):
    try:
        a=cur.fetchone()
        name=a[1]
        ia=imdb.IMDb()
        s_result=ia.search_movie(name)
    #for item in s_result:
    #    print item['long imdb canonical title'], item.movieID

        for the_unt in s_result:
           #print the_unt['title']
           if the_unt['title']==name and the_unt['year']==year:
               # print '----------------------------------------------'+str(kk)+'------'+str(the_unt['title'])+'---------'+str(name)
               # kk=kk+1

              # the_unt=s_result[0]

               ia.update(the_unt,info=('vote details','keywords'))
               ia.update(the_unt)
               # if the_unt['year']!=2009:
               #     continue
               if the_unt.has_key('votes'):
                   if the_unt['votes']<1:
                       #print 'unvalid'
                       continue
                   else:
                       i=i+1
                       # print the_unt['votes']
                       # print the_unt.movieID
                       # print the_unt
                       movieid=the_unt.movieID
                       votes=the_unt['votes']
                       sheet.write(i,12,votes)
                       sheet.write(i,60,movieid)
                       print kk
                       kk=kk+1
               else:
                   continue
               if the_unt.has_key('long imdb canonical title'):
                   #  print the_unt['long imdb canonical title']
                   title=the_unt['long imdb canonical title']
                   sheet.write(i,0,title)

               if the_unt.has_key('year'):
                   # print the_unt['year']
                   year=the_unt['year']
                   sheet.write(i,1,year)

               if the_unt.has_key('countries'):
                   temp=the_unt['countries']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,2,Temp)

               if the_unt.has_key('languages'):
                   temp=the_unt['languages']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,3,Temp)

               if the_unt.has_key('keywords'):
                   temp=the_unt['keywords']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,4,Temp)

               if the_unt.has_key('genres'):
                   temp=the_unt['genres']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,5,Temp)

               if the_unt.has_key('cast'):
                   temp=the_unt['cast']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,6,Temp)

               if the_unt.has_key('editor'):
                   temp=the_unt['editor']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,7,Temp)

               if the_unt.has_key('writer'):
                   temp=the_unt['writer']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,8,Temp)

               if the_unt.has_key('production companies'):
                   temp=the_unt['production companies']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,9,Temp)

               if the_unt.has_key('director'):
                   temp=the_unt['director']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,10,Temp)

               if the_unt.has_key('producer'):
                   temp=the_unt['producer']
                   Temp=[]
                   for temp_count in range(len(temp)):
                       Temp.append(str(temp[temp_count])+'::')
                       temp_count=temp_count+1
                   sheet.write(i,11,Temp)



               if the_unt.has_key('rating'):
                   #print the_unt['rating']
                   rating=the_unt['rating']
                   sheet.write(i,13,rating)

               if the_unt.has_key('number of votes'):
                   #print the_unt['number of votes']
                   number_votes=the_unt['number of votes']
                   for rating in range(1,11):
                       sheet.write(i,rating+13,number_votes[rating])

               if the_unt.has_key('demographic'):
                   #print the_unt['demographic']
                   demo=the_unt['demographic']
                   info=['males','females','aged under 18','males under 18','females under 18',
                         'aged 18-29','males aged 18-29','females aged 18-29','aged 30-44',
                         'males aged 30-44','females aged 30-44','aged 45+',
                         'males aged 45+','females aged 45+','imdb staff','top 1000 voters',
                         'us users','non-us users']
                   for info_count in range (0,36):
                       if info_count%2==1:
                           continue
                       attribution=info[info_count/2]
                       if demo.get(info[info_count/2])!=None:
                           sheet.write(i,info_count+24,demo.get(attribution)[0])
                           sheet.write(i,info_count+25,demo.get(attribution)[1])
                       else:
                           sheet.write(i,info_count+24,None)
                           sheet.write(i,info_count+25,None)

        print 'Now the number is :'+str(number)

        book.save('D:/py/1995data2.xls')
    except:
        print '*******************************************ERROR'
        continue
cur.close()
stop_time = list(time.localtime())
print 'Finished'
print start_time
print stop_time
#time.sleep(60)

