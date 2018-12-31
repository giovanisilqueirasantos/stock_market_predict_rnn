from tensorflow.keras.models import load_model
import numpy as np
from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask import render_template
from flask import url_for
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import time
import threading

recrusul_on = None
cached_data = None

urls = [{
        'name' : 'recrusul_on',
        'url' : 'http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=RCSL3.SA'
    }]

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__, static_url_path='/static')
CORS(app)

cache.init_app(app)

def update_cache_data():
    control = False
    while True:
        if control:
            time.sleep(60)
            control = False

        if datetime.now().hour == 4 and datetime.now().minute == 0 and datetime.now().second == 0:
            control = True
            load_cache()        
        elif datetime.now().hour == 6 and datetime.now().minute == 0 and datetime.now().second == 0:
            control = True
            load_cache()
        elif datetime.now().hour == 8 and datetime.now().minute == 0 and datetime.now().second == 0:
            control = True
            load_cache()

@cache.cached(timeout=None, key_prefix='cached_data')
def cache_data(urls):
    names_data = []
    for url in urls:
        fp = urllib.request.urlopen(url['url'])
        html_bytes = fp.read()
        html_text = html_bytes.decode("utf8")
        fp.close()
        html_parsed = BeautifulSoup(html_text, 'html.parser')

        data = []

        table = html_parsed.find('table', attrs={'class': 'tblCotacoes'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for i in range(3):
            cols = rows[i].find_all('td')
            formated_cols = [
                float(cols[1].text.strip().replace('.', '').replace(',', '.')),
                float(cols[2].text.strip().replace('.', '').replace(',', '.')),
                float(cols[3].text.strip().replace('.', '').replace(',', '.')),
                float(cols[4].text.strip().replace('.', '').replace(',', '.')),
                float(cols[6].text.strip().replace('.', '').replace(',', '.')),
            ]
            data.append(formated_cols)
        names_data.append({'name' : url['name'], 'data' : [[data[2], data[1], data[0]]]})

    return names_data

def load_cache():
    print('Caching data...')
    global cached_data
    cached_data = cache_data(urls)
    print('Data chached!')

def load_models():
    print('Loading models...')
    global recrusul_on
    recrusul_on = load_model('store/recrusul_on.h5')
    recrusul_on._make_predict_function()
    print('Models loaded!')

load_models()
load_cache()
t = threading.Thread(target=update_cache_data)
t.daemon = True
t.start()

@app.route('/', methods=["GET"])
def home():
    url_for('static', filename='grid.css')
    return render_template('index.html')

@app.route("/recrusul-on", methods=["GET"])
def predict():
    global cached_data
    global recrusul_on
    for data in cached_data:
        if data['name'] == 'recrusul_on':
            prediction = recrusul_on.predict(np.array(data['data']), batch_size=None, verbose=0, steps=None).tolist()
            resp = {
                'ok' : True,
                'prediction' : {
                    '1' : round(prediction[0][0], 2),
                    '0' : round(prediction[0][1], 2)
                }
            }
            break
    
    if resp:
        return jsonify(resp)
    else:
        return jsonify({'ok': False, 'error': 'Ops, aconteceu algum problema!'})