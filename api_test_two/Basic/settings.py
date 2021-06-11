#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# 获取项目路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义测试用例的路径
TESTCASE_PATH = os.path.join(BASE_PATH, 'Data')

# 定义测试报告的路径
REPORT_PATH = os.path.join(BASE_PATH, '../yaml_report/')

# 定义日志文件的路径
LOG_PATH = os.path.join(BASE_PATH, 'log/log.txt')

# mysql数据库的连接信息
DB_NAME = 'root'
DB_PASSWORD = 'root'
DB_IP = '39.105.34.24'
PORT = 3306

# redis数据库的连接信息
REDIS_HOST = '192.168.10.46'
REDIS_PORT = 6379
REDIS_PASSWORD = '21cnjycom'




