from case.test_case import TestCase
from setting import REPORT_PATG
from BeautifulReport import BeautifulReport
import unittest
import os


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCase))
    with open(REPORT_PATG, "wb") as f:
        run = BeautifulReport(suite)
        run.report(description='接口测试报告',
                   filename=u"API_report" + ".html",
                   report_dir=os.path.join(os.getcwd(), "yaml_report"))
