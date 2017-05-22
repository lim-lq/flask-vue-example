# coding=utf-8
"""
desc:   utils model

"""
import os


def register_route(api, url_prefix, url_patterns):
    """
    desc:   在主应用中注册模块路由
    params: api             flask_restful 的实例
            url_prefix      路由前缀
            url_patterns    具体的url

    """
    for url in url_patterns:
        if len(url) == 3:
            api.add_resource(url[0], os.path.join(url_prefix, url[1]), endpoint=url[2])
        else:
            api.add_resource(url[0], os.path.join(url_prefix, url[1]))