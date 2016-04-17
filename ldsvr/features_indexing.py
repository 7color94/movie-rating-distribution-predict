#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

redis_ip = 'localhost'
redis_port = 6379
redis_key_indexing_pre = 'mrp:'
redis_key_indexing_suf = ':indexing'
redis_key_counting_suf = ':counting'

categorical_features_theta = {
    'color': 0, 
    'genre': 0, 
    'language': 5, 
    'soundmix': 10, 
    'country':5,
    'actor': 5, 
    'actress': 5,
    'producer': 5, 
    'writer': 5, 
    'cinematographer': 5,
    'composer': 5, 
    'costume designer': 5, 
    'director': 5, 
    'editor': 5, 
    'company': 10,
}


def features_indexing():
    index = 0
    r = redis.Redis(host=redis_ip, port=redis_port)
    pipe = r.pipeline(False)
    for key in categorical_features_theta.keys():
        print 'handing ', key
        fitable_features = r.zrevrangebyscore(name=redis_key_indexing_pre+key+redis_key_counting_suf, max=float('+inf'), min=categorical_features_theta[key], withscores=False)
        print 'find %s fitable_features in %s' % (len(fitable_features), key)
        for f_f in fitable_features:
            pipe.hset(redis_key_indexing_pre+key+redis_key_indexing_suf, f_f, index)
            index = index+1
        pipe.hset(redis_key_indexing_pre+key+redis_key_indexing_suf, key+':others', index)
        index = index+1
        pipe.execute()
    pipe.hset(redis_key_indexing_pre + 'year' + redis_key_indexing_suf, 'year', index)
    index = index+1
    pipe.hset(redis_key_indexing_pre + 'running time' + redis_key_indexing_suf, 'running time', index)
    index = index+1
    pipe.execute()


def run():
    features_indexing()
    print 'features_indexing done.'


if __name__ == '__main__':
    run()