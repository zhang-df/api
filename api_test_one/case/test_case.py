import unittest
import ddt
import codecs
import json
import pytest
import warnings
import os
import logging
from lib.utlis import *
from lib.send_request import Send_requests
from setting import case_root


def case_data(case_name) -> dict:
    """
    :param case_name: 测试用例文件名
    :return: data
    """
    test_case = case_root + '/{}.xlsx'.format(case_name)
    test_num = Excel('r', test_case).read()
    data = excel_header(test_num)
    return data


@ddt.ddt()
class TestCase(unittest.TestCase):

    @ddt.data(*case_data('testcase'))
    def test_case(self, data):
        """
        开整！
        """
        self.response = Send_requests().send_requests(data)
        logging.info('响应内容：%s' % self.response.json())
        print('响应内容：%s' % self.response.json())

        self.result = self.response.json()
        # 判断前置条件是否为1(接口依赖)
        if data['precondition'] == 1:

            # 为1将内容写进test_data文件用来替换下个接口的参数
            with codecs.open(setting.TEST_JSON, 'w', encoding='utf-8') as f:
                json.dump(self.result, f)

            # # 为1调用extract_var,响应保存至全局变量
            # extract_var('w', self.result)

        if int(data['code']) == self.result['code'] and int(
                data['status']) == self.response.status_code and data['message'] == self.result['message']:
            self.msg_data = 'PASS'
            print("message值断言： 预期值：'{}' 实际值：'{}'，断言成功!".format(data['message'], self.result['message']))
            print(self.msg_data)
        else:
            self.msg_data = 'FAIL'
            print("message值断言： 预期值：'{}' 实际值：'{}'，断言失败!".format(data['message'], self.result['message']))
            print(self.msg_data)
        # 将测试结果: result的内容写入Excel
        # Excel('w', results_root) \
        #     .write(write_result(value7=str(self.result), value8=self.msg_data))
        self.assertEqual(self.result['code'], data['code'])
        self.assertEqual(self.response.status_code, data['status'])
        self.assertEqual(self.result['message'], data['message'])
        warnings.simplefilter('ignore', ResourceWarning)


if __name__ == '__main__':
    pytest.main(["-sq",
                 "--alluredir", "../-yaml_report"])
    os.system(r"allure generate --clean allure-results -o allure-yaml_report")
