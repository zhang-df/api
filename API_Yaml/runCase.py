#!/user/bin/env python
# coding=utf-8
"""
pytest用例执行文件
"""

if __name__ == '__main__':
    import pytest
    import os

    pytest.main(['--alluredir', 'allure_report/result'])
    os.system('allure generate allure_report/result -o allure_report/html --clean')
