from flask import Flask, render_template
import logging
import time
from api_1_0_0 import api

app = Flask(__name__)

logtime = time.strftime('%Y-%m-%d', time.localtime())
logging.basicConfig(level=logging.INFO, filename=f'logs/{logtime}.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')

logging.info("Now Starting!")

app.register_blueprint(api, url_prefix='/classpoint')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/log', methods=['GET'])
def GetLog():
    log = open(file=f'logs/{logtime}.log', mode='r')
    log_content = log.read().replace('\n', '<br>')
    return log_content

if __name__ == '__main__':
    app.run()