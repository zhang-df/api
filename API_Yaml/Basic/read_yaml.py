# -*- coding: utf-8 -*-
import yaml
from Basic.settings import *


class ReadData:

    def __init__(self, file_name):
        self.file = os.path.join(TESTCASE_PATH, file_name)

    def return_data(self):
        with open(self.file, 'r', encoding='UTF-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)  # 读取文件内容
            return data
