#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/30 15:23
# @Author: ZhaoKe
# @File : install_packages.py
# @Software: PyCharm
import os
pack_list = [
    # "numpy==1.24.4",
    # "pandas==1.5.3",
    # "openpyxl==3.1.2",
    # "flask==2.3.3",
    # "gevent==24.2.1",
    # "click==8.1.2",
    # "pyecharts",
    "snapshot_selenium",
    # "pymysql==1.1.1",
    # "sqlalchemy==2.0.23",
    # "xlrd",
]
for packa in pack_list:
    os.system("pip install " + packa + " -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com")
