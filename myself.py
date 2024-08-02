#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/31 17:47
# @Author: ZhaoKe
# @File : myself.py
# @Software: PyCharm
from flask import Flask, render_template
from gevent import pywsgi

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'


@app.route('/')
def index():
    return render_template("./myself.html")


if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
