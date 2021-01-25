from app import app
import requests
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    result = requests.get('https://jsonplaceholder.typicode.com/posts').json()
    return render_template('index.html', posts=result)
