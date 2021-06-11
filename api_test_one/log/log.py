import logging
from logging import handlers
from setting import LOG_PATH


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    fh = logging.handlers.TimedRotatingFileHandler(
        filename=LOG_PATH, when='D', interval=1, backupCount=7, encoding='utf-8')
    fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s %(funcName)s:%(lineno)d] - [%(message)s]"
    formatter = logging.Formatter(fmt)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 将处理器添加到日志
    logger.addHandler(sh)
    logger.addHandler(fh)


if __name__ == '__main__':
    init_logging()
    logging.info('——————————————你2020必暴富——————————————————')
