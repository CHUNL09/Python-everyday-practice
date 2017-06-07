#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from conf import sys_config


class logger(object):
    def __init__(self):
        self.log_file=sys_config.LOG_FILE
        self.log_format=sys_config.LOG_FORMAT
        self.log_level=sys_config.LOG_LEVEL

    def log(self):
        logger=logging.getLogger('ops_logger')
        logger.setLevel(self.log_level)
        formatter=logging.Formatter(self.log_format)

        #ch=logging.StreamHandler()
        #ch.setLevel(self.log_level)

        fh=logging.FileHandler(self.log_file)
        #fh.setLevel(self.log_level)

        #ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        #logger.addHandler(ch)
        return logger