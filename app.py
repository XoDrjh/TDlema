from flask import Flask, render_template
import logging
import time
from api_1_0_0 import api

app = Flask(__name__)

# log文件以日期命名
logtime = time.strftime('%Y-%m-%d', time.localtime())
logging.basicConfig(level=logging.INFO, filename=f'logs/{logtime}.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')

# log写入成功运行信息
logging.info("Now Starting!")

# 注册api蓝图对象，URL前缀为“/classpoint”
app.register_blueprint(api, url_prefix='/classpoint')

# 首页
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 查看log
@app.route('/log', methods=['GET'])
def GetLog():
    log = open(file=f'logs/{logtime}.log', mode='r')
    log_content = log.read().replace('\n', '<br>')
    return log_content

if __name__ == '__main__':
    app.run()