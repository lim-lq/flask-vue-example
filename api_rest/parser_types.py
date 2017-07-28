# coding=utf-8
"""
desc:   自定义flask-restful reqparse的参数类型检测函数
author: congqing.li
date:   2016-11-10

"""


def string(length):
    """
    desc:   字符串类型
    params: length  字符串长度
    return: True    合法
            False   非法

    """
    def _decorator(data):
        """
        desc:   闭包函数
        params: data    带检测的数据

        """
        if isinstance(data, unicode):
            pass
        elif isinstance(data, str):
            pass
        else:
            try:
                data = str(data)
            except:
                raise ValueError("Must be string")

        if len(data) > length:
            raise ValueError("Must be less then %s bytes" % length)
        return data

    return _decorator
