import requests
import logging

from data.data_driver import load_data, Global_
from lib.utlis import get_host


class Send_requests:

    def __init__(self):
        self.session = requests.session()

    def send_requests(self, apidata):
        """
        :param apidata: 字典类型
        :return: req
        """
        body_data = Global_().save_text(load_data(), apidata['data'])
        res = self.session.request(method=apidata["method"],
                                   url=get_host('loc') + apidata["path"],
                                   headers=apidata['header'],
                                   params=eval(body_data))
        logging.info('请求参数：%s' % format(body_data))
        print('请求参数：%s' % format(body_data))
        return res


if __name__ == '__main__':
    case_dict = {
        'id': 1.0,
        'method': 'post',
        'interface': 'login',
        'title': '参数正常-成功',
        'header': {'Cookie': '$..data.access_token'},
        'precondition': 1,
        'path': '/api/user/login?',
        'data': "{'account':'11025688', 'password':'a123456', 'baseid':0, 'schoolid':461361, 'access_token': '$..data.access_token'}",
        'expected': "{'code': 0, 'message': '登陆成功'}",
        'code': 0,
        'status': 200.0,
        'msg': '登陆成功',
        'jsonpath': ''}
    re = Send_requests().send_requests(case_dict)
