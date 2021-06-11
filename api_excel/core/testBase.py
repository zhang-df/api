# coding=utf-8
import requests
import jsonpath
import re
import allure
import json
from json import dumps
from core.logger import Logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

logger = Logger().logger

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BaseTest(requests.Session):
    """
    接口基类
    verify断言：JSONPATH=预期结果
    示例: .msg=操作成功; .code=0
    """

    def get_request(self, url, headers=None, params=None, cookies=None):
        """
        get请求方法
        :param url: 地址
        :param headers: 请求头
        :param params: 请求参数
        :param cookies:
        :return:
        """
        try:
            res = self.request('GET', url, headers=headers, params=params, cookies=cookies, verify=False)
            self.api_log('GET', url, headers=headers, params=params, cookies=cookies,
                         code=res.status_code, res_text=res.content, res_header=res.headers)
            return res
        except Exception as e:
            logger.error("接口请求异常,原因：{}".format(e))
            raise e

    def post_request(self, url, headers=None, data=None, json=None, params=None, cookies=None):
        """
        post请求方法
        :param url: 接口地址
        :param headers: 请求头
        :param json: 请求体
        :param params: 请求参数
        :param cookies:
        :return:
        """
        try:
            res = self.request('POST', url, headers=headers, params=params, data=data,
                               json=json, cookies=cookies, verify=False)
            self.api_log('POST', url, headers=headers, params=params, json=json, cookies=cookies,
                         code=res.status_code, res_text=res.content, res_header=res.headers)
            return res

        except Exception as e:
            logger.error("接口请求异常,原因：{}".format(e))
            raise e

    def upload_request(self, url, headers=None, data=None, files=None, json=None, params=None, cookies=None):
        try:
            filename = list(files.keys())[0]
            filepath = list(files.values())[0]
            with open(filepath, 'rb') as file:
                files["{}".format(filename)] = file
                res = self.request('POST', url, headers=headers, params=params, data=data,
                                   files=files, json=json, cookies=cookies, verify=False)
            self.api_log('UPLOAD', url, headers=headers, params=params, json=data, file=filepath, cookies=cookies,
                         code=res.status_code, res_text=res.content, res_header=res.headers)
            return res

        except Exception as e:
            logger.error("接口请求异常,原因：{}".format(e))
            raise e

    def assertEquals(self, actual, expected):
        """
        断言是否等于
        :param actual: 实际值
        :param expected: 预期值
        :return:
        """
        try:
            assert actual == expected
            logger.info("断言： 预期值：'{}' 实际值：'{}', 断言成功!".format(expected, actual))
        except AssertionError:
            logger.error("断言： 预期值：'{}' 实际值：'{}', 断言失败!".format(expected, actual))
            raise AssertionError

    def assertTrue(self, actual):
        """
        断言是否为真
        :param actual: 实际值
        :return:
        """
        try:
            assert actual
            logger.info("断言： 实际值：'{}' 为真, 断言成功!".format(actual))
        except AssertionError as e:
            logger.error("断言： 实际值：'{}' 不为真, 断言失败!".format(actual))
            raise e

    def assertIn(self, content, target):
        """
        断言是否包含
        :param content: 包含文本
        :param target: 目标文本
        :return:
        """
        try:
            assert content in target
            logger.info("断言： 目标文本：'{}' 包含 文本：'{}', 断言成功!".format(target, content))
        except AssertionError as e:
            logger.error("断言： 目标文本：'{}' 不包含 文本：'{}', 断言失败!".format(target, content))
            raise e

    def api_log(self, method, url, headers=None, params=None, json=None, cookies=None, file=None, code=None,
                res_text=None, res_header=None):
        logger.info("请求方式====>{}".format(method))
        logger.info("请求地址====>{}".format(url))
        if headers:
            logger.info("请求头为====>{}".format(dumps(headers, indent=4)))
        logger.info("请求参数====>{}".format(dumps(params, indent=4)))
        if json:
            logger.info("请求内容====>{}".format(dumps(json, indent=4, ensure_ascii=False)))
        if file:
            logger.info("上传附件为======>{}".format(file))
        if cookies:
            logger.info("接口Cookie====>{}".format(dumps(cookies, indent=4)))
        logger.info("响应状态码为====>{}".format(code))
        logger.info("接口响应头为====>{}".format(res_header))
        logger.info("接口响应内容====>{}".format(res_text.decode("utf-8")))


class Global:
    """
    接口依赖
    将响应字段存到参数池: key=JSONPATH
    调用参数池的字段内容: ${key}
    """

    def __init__(self):
        global saves  # 全局变量池
        global EXPR  # 识别${key}的正则表达式
        global FUNC_EXPR  # 识别函数助手
        self.saves = {}
        self.EXPR = r'\$\{(.*?)\}'
        self.FUNC_EXPR = r'__.*?\(.*?\)'

    def save_data(self, source, key, jsz):
        """
        提取参数并保存至全局变量池
        :param source: 目标字符串
        :param key: 全局变量池的key
        :param jsz: 判断Json表达式还是正则表达式
        :return:
        """
        if jsz.startswith("$."):
            value = jsonpath.jsonpath(source, jsz)[0]
        else:
            if len(re.findall(jsz, source.text)) == 1:
                value = re.findall(jsz, source.text)[0]
            else:
                value = []
                for i in range(len(re.findall(jsz, source.text))):
                    value.append(re.findall(jsz, source.text)[i])
        if value:
            self.saves[key] = value
            logger.info("保存 {}=>{} 到全局变量池".format(key, value))
        else:
            logger.error("保存失败，参数为空")

    def build_param(self, _string):
        """
        识别${key}并替换成全局变量池的value,处理__func()函数助手
        :param _string : 待替换的字符串
        :return:
        """

        # 遍历所有取值并做替换
        keys = re.findall(self.EXPR, _string)
        for key in keys:
            if type(self.saves.get(key)) == list:
                num = int(_string.split('[')[1].split(']')[0])
                value = self.saves.get(key)[num]
                _string = _string.replace('[%s]' % num, '')
            else:
                value = self.saves.get(key)
            _string = _string.replace('${' + key + '}', str(value))

        # 遍历所有函数助手并执行，结束后替换
        funcs = re.findall(self.FUNC_EXPR, _string)
        for func in funcs:
            fuc = func.split('__')[1]
            fuc_name = fuc.split("(")[0]
            fuc = fuc.replace(fuc_name, fuc_name.lower())
            value = eval(fuc)
            _string = _string.replace(func, str(value))
        return _string

    def execute_setup_sql(self, db_connect, setup_sql):
        """
        执行setup_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param setup_sql: 前置sql
        :return:
        """
        for sql in [i for i in setup_sql.split(";") if i != ""]:
            result = db_connect.execute_sql(sql)
            if sql.lower().startswith("select"):
                logger.info("执行前置sql====>{}，获得以下结果集:{}".format(sql, result))
                # 获取所有查询字段，并保存至公共参数池
                for key in result.keys():
                    self.saves[key] = result[key]
                    logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))

    def execute_teardown_sql(self, db_connect, teardown_sql):
        """
        执行teardown_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param teardown_sql: 后置sql
        :return:
        """
        for sql in [i for i in teardown_sql.split(";") if i != ""]:
            result = db_connect.execute_sql(sql)
            if sql.lower().startswith("select"):
                logger.info("执行后置sql====>{}，获得以下结果集:{}".format(sql, result))
                # 获取所有查询字段，并保存至公共参数池
                for key in result.keys():
                    self.saves[key] = result[key]
                    logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))

    def execute_redis_get(self, redis_connect, keys):
        """
        读取redis中key值,并保存结果至参数池
        :param redis_connect: redis实例
        :param keys:
        :return:
        """
        for key in [key for key in keys.split(";") if key != ""]:
            value = redis_connect.get(key)
            self.saves[key] = value
            logger.info("保存 {}=>{} 到全局变量池".format(key, value))


def allure_(api_data):
    """
    :param api_data: apidata
    :return:
    """
    allure.dynamic.suite(api_data['descrption']['descrption'])
    allure.dynamic.sub_suite(api_data['descrption']['sub_suite'])
    allure.dynamic.feature(api_data['descrption']['feature'])
    allure.dynamic.story(api_data['descrption']['story'])
    allure.dynamic.title(api_data['descrption']['descrption'])
    allure.dynamic.issue(api_data['url'])
