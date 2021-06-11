# coding=utf-8

import pytest




class Abc:

    def access_token(self):
        return {
            'descrption': '获取access_token',
            'url': 'http://api.21szxy.com/api/auth/access_token?app_id=client_id&app_secret=client_secret',
            'method': 'GET',
            'headers': '',
            'cookies': '',
            'params': '',
            'body': '',
            'saves': 'access_token=$..data.access_token',
            'verify': '$.message=获取成功!;$.code=0',
            'dbtype': '',
            'db': '',
            'setup_sql': '',
            'teardown_sql': '',
            'file': ''}

    def login_succeed(self):
        return {
            'descrption': '参数正常-成功',
            'url': 'http://api.21szxy.com/api/user/login?',
            'method': 'GET',
            'headers': '',
            'cookies': '',
            'params': "{'access_token': '${access_token}','account': '11025688','password': 'a123456','baseid': 0,'schoolid': 461361}",
            'body': '',
            'saves': '',
            'verify': '$.message=登陆成功',
            'dbtype': '',
            'db': '',
            'setup_sql': '',
            'teardown_sql': '',
            'file': ''}

    def login_error(self):
        return {
            'descrption': '登陆参数错误-失败',
            'url': 'http://api.21szxy.com/api/user/login?',
            'method': 'GET',
            'headers': '',
            'cookies': '',
            'params': "{'access_token': '${access_token}', 'account':110256880, 'password':'a123456', 'baseid':0, 'schoolid':461361}",
            'body': '',
            'saves': '',
            'verify': '$.message=账号或密码错误',
            'dbtype': '',
            'db': '',
            'setup_sql': '',
            'teardown_sql': '',
            'file': ''}

    def login_null(self):
        return {
            'descrption': '登陆参数为空-失败',
            'url': 'http://api.21szxy.com/api/user/login?',
            'method': 'GET',
            'headers': '',
            'cookies': '',
            'params': "{'access_token': '${access_token}', 'account':'', 'password':'a123456', 'baseid':0, 'schoolid':461361}",
            'body': '',
            'saves': '',
            'verify': '$.message=传如参数有误',
            'dbtype': '',
            'db': '',
            'setup_sql': '',
            'teardown_sql': '',
            'file': ''}


@pytest.fixture(scope='session')
def login_null():
    return {
        'descrption': '登陆参数为空-失败',
        'url': 'http://api.21szxy.com/api/user/login?',
        'method': 'GET',
        'headers': '',
        'cookies': '',
        'params': "{'access_token': '${access_token}', 'account':'', 'password':'a123456', 'baseid':0, 'schoolid':461361}",
        'body': '',
        'saves': '',
        'verify': '$.message=传如参数有误',
        'dbtype': '',
        'db': '',
        'setup_sql': '',
        'teardown_sql': '',
        'file': ''}
