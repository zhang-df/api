# -*- coding: utf-8 -*-
from core.readExcel import *
from core.testBase import *
import allure
import pytest
from core.functions import *
from db_operate.mysql_operate import MySQLOperate
from db_operate.redis_operate import RedisOperate


def case_data():
    """
    :return: list_data
    """
    excel_data = ReadExcel().read_excel()
    list_data = ReadExcel().excel_header(excel_data)
    return list_data


class TestClass:
    global_ = Global()

    @classmethod
    def setup_class(cls):
        # 实例化测试基类，自带cookie保持
        cls.request = BaseTest()

    @allure.suite('数字化校园')
    @allure.sub_suite('登陆及学生模块')
    @allure.feature('数字化校园')
    @allure.story('登陆及学生模块')
    @pytest.mark.parametrize('api_data', case_data())
    def test_run(self, api_data):
        allure.dynamic.title(api_data['descrption'])
        allure.dynamic.issue(api_data['url'])
        logger.info("用例描述====>" + api_data['descrption'])
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
                # 切割字符串 如 key=$.data
                key = save.split("=")[0]
                jsp = save.split("=")[1]
                self.global_.save_data(res.json(), key, jsp)

        if api_data['verify']:
            # 遍历verify:
            for ver in api_data['verify'].split(";"):
                expr = ver.split("=")[0]
                # 判断Jsonpath还是正则断言
                if expr.startswith("$."):
                    actual = jsonpath.jsonpath(res.json(), expr)
                    if not actual:
                        logger.error("该jsonpath未匹配到值,请确认接口响应和jsonpath正确性")
                    actual = actual[0]
                else:
                    actual = re.findall(expr, res.text)[0]
                expect = ver.split("=")[1]
                self.request.assertEquals(str(actual), expect)

        # 最后关闭mysql数据库连接
        if db_connect:
            db_connect.db.close()

    @classmethod
    def teardownclass(cls):
        pass


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
