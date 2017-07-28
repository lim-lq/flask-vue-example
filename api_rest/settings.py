# coding=utf-8
"""
desc:   project config file
author: lev-lq
date:   2017-05-23

"""

# 数据库配置
# 连接的url，配置的用户需要所有权限
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/db"

# 刷新数据库连接，防止mysql在没有交互的时候断开连接，单位秒（s）
SQLALCHEMY_POOL_RECYCLE = 3600

# 数据库连接池大小
SQLALCHEMY_POOL_SIZE = 20

# 默认
SQLALCHEMY_TRACK_MODIFICATIONS = True

# celery配置
CELERY_BROKER_URL = "redis://127.0.0.1:6379/3"
CELERY_BACKEND_URL = "redis://127.0.0.1:6379/3"
CELERYD_HIJACK_ROOT_LOGGER = False
# 后台并行任务数
CELERYD_CONCURRENCY = 8

# 缓存配置
REDIS_URL = "redis://localhost:6379/4"

# 用户登录的Token过期时间,单位秒
USER_TOKEN_EXPIRATION = 60 * 60 * 24 * 30
