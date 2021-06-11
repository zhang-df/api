# -*- coding: utf-8 -*-
import pytest
import json
from Basic.read_yaml import *
from Basic.testBase import *
from db_operate.mysql_operate import MySQLOperate
from db_operate.redis_operate import RedisOperate
scale = 156


def case_data():
    """
    :return: list_data
    """
    file = os.listdir(TESTCASE_PATH)
    list_data = []
    for i in file:
        yaml_data = ReadData(i).return_data()  # 返回yaml文件读取数据
        for key, value in yaml_data.items():
            list_data.append(value['api_data'])
    return list_data


class TestClass:
    global_ = Global()

    @classmethod
    def setup_class(cls):
        # 实例化测试基类，自带cookie保持
        cls.request = BaseTest()

    @pytest.mark.parametrize('api_data', case_data())
    def test_case(self, api_data):
        allure_(api_data)
        logger.info("用例描述====>" + api_data['descrption']['descrption'])
        db_connect = None
        redis_db_connect = None
        setup_sql = self.global_.build_param(api_data['setup_sql'])
        teardown_sql = self.global_.build_param(api_data['teardown_sql'])

        # 判断数据库类型,mysql or redis
        if api_data['dbtype'].lower() == "mysql":
            db_connect = MySQLOperate(api_data['db'])
        elif api_data['dbtype'].lower() == "redis":
            redis_db_connect = RedisOperate(api_data['db'])
        else:
            pass

        if db_connect:
            # 执行teardown_sql
            self.global_.execute_setup_sql(db_connect, setup_sql)

        if redis_db_connect:
            # 执行teardown_redis操作
            self.global_.execute_redis_get(redis_db_connect, teardown_sql)

        url = self.global_.build_param(api_data['url'])
        headers = self.global_.build_param(api_data['headers'])
        params = self.global_.build_param(api_data['params'])
        body = self.global_.build_param(api_data['body'])
        params = eval(params) if params else params
        headers = eval(headers) if headers else headers
        cookies = eval(api_data['cookies']) if api_data['cookies'] else api_data['cookies']
        body = eval(body) if body else body
        file = eval(api_data['file']) if api_data['file'] else api_data['file']

        # 判断接口请求类型
        if api_data['method'].upper() == 'GET':
            res = self.request.get_request(url=url, params=params, headers=headers, cookies=cookies)
        elif api_data['method'].upper() == 'POST':
            res = self.request.post_request(url=url, headers=headers, cookies=cookies, params=params, json=body)
        elif api_data['method'].upper() == 'UPLOAD':
            res = self.request.upload_request(url=url, headers=headers, cookies=cookies, params=params, data=body,
                                              files=file)
        else:
            pass

        if db_connect:
            # 执行teardown_sql
            self.global_.execute_teardown_sql(db_connect, teardown_sql)

        if api_data['saves']:
            # 遍历saves
            for save in api_data['saves'].split(";"):
                if "$." in api_data['saves']:
                    key = save.split("=")[0]
                    jsp = save.split("=")[1]
                    self.global_.save_data(res.json(), key, jsp)
                else:
                    key = save.split(",")[0]
                    jsp = save.split(",")[1]
                    self.global_.save_data(res, key, jsp)

        if api_data['verify']:
            # 遍历verify:
            for ver in api_data['verify'].split(";"):
                # 判断Jsonpath还是正则断言
                if "$." in ver:
                    expr = ver.split("=")[0]
                    actual = jsonpath.jsonpath(res.json(), expr)
                    if not actual:
                        logger.error("该jsonpath未匹配到值,请确认接口响应和jsonpath正确性")
                    actual = actual[0]
                    expect = ver.split("=")[1]
                else:
                    actual = re.findall(ver, res.text)[0]
                    expect = ver
                self.request.assertEquals(str(actual), expect)

        # 最后关闭mysql数据库连接
        if db_connect:
            db_connect.db.close()

    # def teardown_class(self):
    #     print('test end'.center(scale // 2, "="))


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
