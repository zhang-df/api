import xlrd
from openpyxl import load_workbook
import setting
import ast


class Excel:

    def __init__(self, type, file_name):
        """
        初始化方法
        :param type: r:读 w:写
        :param file_name: 文件路径
        """
        if type == 'r':
            self.workbook = xlrd.open_workbook(file_name)
            self.sheet_names = self.workbook.sheet_names()
            self.list_data = []
        elif type == 'w':
            self.filename = file_name
            self.wb = load_workbook(self.filename)
            self.ws = self.wb.active
            self.wb.close()

    def read(self) -> list:
        for sheet_name in self.sheet_names:
            sheet = self.workbook.sheet_by_name(sheet_name)
            for i in range(sheet.nrows):
                if sheet.row_values(i)[0] != '用例编号':    # 是否忽略首行
                    row_values = sheet.row_values(i)
                    row_values[6] = ast.literal_eval(row_values[6])
                    self.list_data.append(row_values)
        return self.list_data

    def write(self, data):
        """
        数据写入excel内
        :param data: 需要写入的数据: list
        :return:
        """
        self.ws.append(data)
        self.wb.save(self.filename)

def excel_header(data):
    """
    1.将excel头部替换成英文的
    2.处理成json/dict
    """
    header = {
        '用例编号': 'id',
        '请求方法': 'method',
        '用例标题': 'descrption',
        '请求头': 'header',
        '前置条件': 'precondition',
        '接口path': 'path',
        '测试数据': 'data',
        '预期结果': 'expected',
        'json返回code': 'code',
        '状态码': 'status',
        '响应状态': 'message',
        'jsonPath表达式': 'jsonpath'
    }
    head = list(header.values())
    list_dict = []
    for i in data:
        if i[0] != '':
            dict_data = {}
            for j in range(len(head)):
                dict_data[head[j]] = i[j]
            list_dict.append(dict_data)
        else:
            pass
    return list_dict

def write_result(value1=None, value2=None, value3=None,
                 value4=None, value5=None, value6=None,
                 value7=None, value8=None) -> list:
    """
    将写入的值返回 (list格式)
    :return:
    """
    result_list = []
    result_list.append(value1)
    result_list.append(value2)
    result_list.append(value3)
    result_list.append(value4)
    result_list.append(value5)
    result_list.append(value6)
    result_list.append(value7)
    result_list.append(value8)
    return result_list

def get_host(value):
    """
    返回不同环境的host
    :param loc：本地环境 uat: uat环境 dev: 开发环境
    :return: path
    """
    if value == 'dev':
        return setting.BASE_URL_dev
    elif value == 'uat':
        return setting.BASE_URL_uat
    elif value == 'loc':
        return setting.BASE_URL_loc
    else:
        print('host切到:%s? 你怎么不切换到天上去？' % format(value))

if __name__ == '__main__':
    file = '../database/testcase.xlsx'
    from pprint import pprint
    pprint(excel_header(Excel('r', file).read()))
    print(len(excel_header(Excel('r', file).read())))
    print(type(excel_header(Excel('r', file).read())))
