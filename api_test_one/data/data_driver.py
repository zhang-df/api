import setting
import re
import jsonpath


def load_data() -> dict:
    """
    返回test_data内的数据
    :return: dict
    """
    with open(setting.TEST_JSON, encoding='utf-8')as obj:
        for line in obj:
            token_data = eval(line)
            return token_data


class Global_():
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

    def save_data(self, source, key, jexpr):
        """
        提取参数并保存至全局变量池
        :param source: 目标字符串
        :param key: 全局变量池的key
        :param jexpr: jsonpath表达式
        :return:
        """
        value = jsonpath.jsonpath(source, jexpr)
        if value:
            self.saves[key] = value[0]
            print("保存 {}=>{} 到全局变量池".format(key, value))
        else:
            print("保存失败，参数为空")

    def build_param(self, _string):
        """
        识别${key}并替换成全局变量池的value,处理__func()函数助手
        :param _string:
        :param _string : 待替换的字符串
        :return:
        """

        # 遍历所有取值并做替换
        keys = re.findall(self.EXPR, _string)
        for key in keys:
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

    def save_text(self, replace_data, request_data):
        """
        提取参数并保存至txt文本(已放弃)
        :param replace_data: 上个接口返回的数据
        :param request_data: 当前接口的请求数据
        :return: str
        """
        keys = re.findall(re.compile(r"'\$..([\s\S]+?)'"), str(request_data))
        if keys:
            for key, values in request_data.items():
                if jsonpath.jsonpath(replace_data, str(values)):
                    if '$..' in values:
                        values = values.lstrip('$..')
                        if '.' in values:
                            request_data[key] = replace_data[values.split(
                                '.')[0]][values.split('.')[1]]
                        else:
                            request_data[key] = replace_data[values]
                    else:
                        request_data[key] = replace_data[key]
            return str(request_data)
        else:
            return str(request_data)


if __name__ == '__main__':
    """
    用data代替replace_data内的parameter
    """
    replace_data = "{'data': {'access_token': 'Bj/7Asbw3x5dCpvTFTo9GXGgSgXXD3Lh1iapPOs7y/HH23DhwGuMhBxYWYac7vJG', 'expires_in': 86400}, 'message': '获取成功!', 'code': 0}"
    request_data = "{'access_token': '$..data.access_token','openids': ['12017331'],'operaUser': 11025688}"
    print('被替换的参数:', load_data())
    print('替换前的参数:', request_data)
    print('替换后的参数:', data_association(load_data(), request_data))
