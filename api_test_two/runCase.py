#!/user/bin/env python
# coding=utf-8
"""
pytest用例执行文件
"""

if __name__ == '__main__':
    import pytest
    import os

    pytest.main(['--alluredir', 'yaml_report/result', 'testcase/test_case.py'])
    split = 'allure generate yaml_report/result --clean -o yaml_report/html --clean'
    os.system(split)
