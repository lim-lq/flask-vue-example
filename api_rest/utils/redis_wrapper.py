#coding=utf-8
"""
desc:   redis包装模块
author: congqing.li
date:   2016-07-19

"""
import redis


class Redis(object):
    def __init__(self, redis_url):
        self._conn = redis.Redis(connection_pool=redis.ConnectionPool.from_url(redis_url))

    def set(self, expire=None, **kwargs):
        """
        desc:   设置缓存键值

        """
        for key in kwargs:
            self._conn.set(key, kwargs[key], ex=expire)

        return True

    def get(self, key, eval_=False):
        """
        desc:   获取缓存值
        params: key     键值
                eval_   获取的数据是否通锅eval转换

        """
        if eval_:
            return eval(self._conn.get(key))
        else:
            return self._conn.get(key)

    def delete(self, key):
        """
        desc:   删除缓存键值

        """
        self._conn.delete(key)

    def hset(self, key, field, value):
        """
        desc:   设置字典键值
        params:

        """
        return self._conn.hset(key, field, value)

    def hget(self, key, field, evalable=False):
        """
        desc:   获取字典键值

        """
        data = self._conn.hget(key, field)

        if data and evalable:
            return eval(data)
        return data