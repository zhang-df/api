import os

BASE_URL_loc = "http://api.21szxy.com"  # 本地环境
BASE_URL_dev = 'http://api.21szxy.com'  # dev环境
BASE_URL_uat = 'http://api.21szxy.com'  # uat环境

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# 测试用例的目录
case_root = os.path.join(PROJECT_ROOT, 'database')
# 测试结果的目录
results_root = os.path.join(PROJECT_ROOT, 'results', 'results.xlsx')
# 日志的目录
LOG_PATH = os.path.join(PROJECT_ROOT, 'log', 'api_test.log')
# 报告的目录
REPORT_PATG = os.path.join(PROJECT_ROOT, 'yaml_report', 'API_report.html')  # 报告
# 存放接口返回数据
TEST_JSON = os.path.join(PROJECT_ROOT, 'database', 'test_data.txt')
