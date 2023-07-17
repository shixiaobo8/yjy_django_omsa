#! /usr/bin/env python
# -*- coding:utf8 -*-

"""
    阿里云sdk client 类
"""
from aliyunsdkcore import client

class ali_client(object):    
      
    def __init__(self):
        self.config = ('xxxxxxxx','xxxxxxxxxxxxxxxxxx','cn-shenxi')
        self.alt = client.AcsClient(self.config[0],self.config[1],self.config[2])
        
    def getClient(self):
        return self.alt
