from bp_update.routes import update_app
from bp_auth.routes import auth_app
from bp_query.routes import request_app
from bp_basket.routes import basket_app

import json

from flask import Flask, render_template, session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['DB_CONFIG'] = json.load(open('configs/db.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))


app.register_blueprint(request_app, url_prefix='/request')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(update_app, url_prefix='/update')
app.register_blueprint(basket_app, url_prefix='/basket')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exit')
def exit():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
