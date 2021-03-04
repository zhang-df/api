# coding=utf-8
import xlrd
from core.settings import *


class ReadExcel(object):

    def __init__(self):
        self.path = os.path.join(BASE_PATH + "/conf/case.xlsx")

    def read_excel(self):
        """
        读取excel文件内容:
        description:用例描述
        url:接口地址
        method:请求方式 GET or POST
        headers:请求头,格式为 {"key","value"}
        cookies:Cookies,格式为 {"key":"value"}
        params:请求参数,格式为 {"key":"value"}
        body:请求体,格式为 {"key":"value"}
        file:请求文件,格式为 {"key":"文件名称"} 文件需放到框架的files目录下
        verify:断言,格式为 JSONPATH=预期结果
        saves:关联,格式为 自定义key=JSONPATH
        dbtype:数据库类型,目前支持mysql/redis
        db:数据库名称
        setup_sql:前置数据库语句(在用例执行前执行):
        若为mysql,直接写sql即可,可支持执行多条sql,用分号隔开,若是查询语句则会将查询的字段存储到公共变量池;
        若为redis,则写形如key1;key2;key3,会进行redis查询并储存变量
        teardown_sql:后置数据库语句(在用例执行后执行),用法如上
        """
        workbook = xlrd.open_workbook(self.path)
        sheet_names = workbook.sheet_names()
        list_data = []
        for sheet_name in sheet_names:
            sheet = workbook.sheet_by_name(sheet_name)
            for i in range(sheet.nrows):
                if sheet.row_values(i)[0] != '用例编号':  # 是否忽略首行
                    row_values = sheet.row_values(i)
                    list_data.append(row_values)
        return list_data

    def excel_header(self, data):
        """
        1.将excel头部替换成英文
        2.处理成json/dict
        """
        header = {
            '用例描述': 'descrption',
            '请求url': 'url',
            '请求方法': 'method',
            '请求头部': 'headers',
            'cookies': 'cookies',
            'params': 'params',
            'json': 'body',
            'saves': 'saves',
            'verify': 'verify',
            'dbtype': 'dbtype',
            'db': 'db',
            'setup_sql': 'setup_sql',
            'teardown_sql': 'teardown_sql',
            'file': 'file'
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


if __name__ == '__main__':
    test = ReadExcel().read_excel()
    print(test)
    data = ReadExcel().excel_header(ReadExcel().read_excel())
    print(data)
