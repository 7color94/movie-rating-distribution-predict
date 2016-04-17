#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import numpy as np

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '1227401054'
mysql_db = 'mrp'
conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')

def write_test_dis_todb():
    cur = conn.cursor()
    testDistribution = np.loadtxt('testPredict.txt')
    testId = np.loadtxt('testId.txt')
    print 'testDistribution shape:', testDistribution.shape
    print 'testId shape:', testId.shape
    for (row, m_id) in zip(testDistribution, testId):
        print 'inserting ', m_id
        cur.execute("INSERT INTO new_movies_voting values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (int(m_id), float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]))
                    )
        conn.commit()
    cur.close()

def run():
    write_test_dis_todb()
    conn.close()

if __name__ == '__main__':
    run()