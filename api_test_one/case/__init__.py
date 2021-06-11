import logging
from log.log import init_logging

# 环境切换 loc,dev,uat
surroundings = 'loc'

init_logging()
logging.info("测试日志信息👇|{}环境".format(surroundings))