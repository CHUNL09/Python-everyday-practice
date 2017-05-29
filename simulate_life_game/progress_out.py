# -*- coding:utf-8 -*-

"""
定义Progress_out类，主要实现进度条打印和文字的单个输出
"""

import sys,time

class Progress_out(object):
    def __init__(self,p_sign,p_interval,p_range,w_interval):
        self.p_sign=p_sign
        self.p_interval=p_interval
        self.p_range=p_range
        self.w_interval=w_interval

    def generate_progress_bar(self):
        """
        实现进度条的打印
        :param expression:
        :return:
        """
        j=self.p_sign
        for i in range(1,self.p_range):
            j += self.p_sign
            progress=int((i/60)*100)
            sys.stdout.write("loading: %s%% %s\r" %(progress,j))
            sys.stdout.flush()
            time.sleep(self.p_interval)

    def generate_progress_sentence(self,p_str):
        """
        实现文字的单个输出
        :param expression: p_str-传入的字符串
        :return:
        """
        for i in range(len(p_str)):
            sys.stdout.write(p_str[i])
            sys.stdout.flush()
            time.sleep(self.w_interval)