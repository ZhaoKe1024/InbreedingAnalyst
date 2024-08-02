#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/2 11:47
# @Author: ZhaoKe
# @File : __init__.py.py
# @Software: PyCharm
from flask import Flask
# 创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
from app import routes
