from flask import render_template, g, Flask

from data_base.fdatabase import FDataBase
from config import Config

import sqlite3, os

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'mainbase.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.route('/', methods=['POST', 'GET'])
def index_page():
    db = get_db()
    database = FDataBase(db)
    return render_template('index.html', data=database.getData())

if __name__ == '__main__':
    app.run(debug=True)