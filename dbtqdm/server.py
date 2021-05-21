from typing import List

from flask import Flask, request, render_template
from flask_cors import CORS
from logging import getLogger

from pymongo.database import Database

from dbtqdm import connect_db
from dbtqdm.args.server import TqdmArgParser
from dbtqdm.consts import DEF_TITLE, DEF_INTERVAL, DEF_DB_PORT, DEF_HOST, DEF_PORT, DEF_DB_HOST, DEF_DB_NAME, \
    STATS_COLLECTION

app = Flask(__name__, template_folder='pages')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
logger = getLogger(__name__)
TQDM_ROUTE, STATS_ROUTE = '/tqdm', '/stats'
web_title, interval = DEF_TITLE, DEF_INTERVAL * 1000


@app.route('/')
def home() -> str:
    """ The home page, which shows some help. """
    global web_title, interval
    return render_template('index.html', title=web_title, interval=interval)


@app.route('/health')
def health():
    """ Check if this service is alive. """
    return "I am ready!"


def bar_progress(db: Database, bar_name: str) -> dict:
    bar = db[bar_name].find_one({})
    if bar and '_id' in bar:
        del bar['_id']
        bar['bar_name'] = bar_name
    return bar


@app.route(TQDM_ROUTE + '/<bar_name>', methods=['GET'])
def tqdm(bar_name: str = None) -> List[dict]:
    global db
    if bar_name:
        return bar_progress(db, bar_name)
    return [bar_progress(db, name) for name in db.getCollectionNames()]


@app.route(TQDM_ROUTE, methods=['GET'])
def all_progress_bars() -> List[dict]:
    global db, web_title
    return {
        'title': web_title,
        'bars': [bar_progress(db, name) for name in db.collection_names() if name != STATS_COLLECTION]
    }


def start_server(title: str = DEF_TITLE, host: str = DEF_HOST, port: int = DEF_PORT,  db_host: str = DEF_DB_HOST,
                 db_port: int = DEF_DB_PORT, replicaset: str = None, db_name: str = DEF_DB_NAME,
                 seconds_interval: int = DEF_INTERVAL * 5000) -> None:
    global db, web_title, interval
    web_title, interval = title, seconds_interval
    client = connect_db(db_host, db_port, replicaset)
    db = client[db_name]
    app.run(host, port)


def main() -> None:
    args = TqdmArgParser()
    start_server(args.title, args.host, args.port, args.db_host, args.db_port, args.replicaset, args.database)


if __name__ == '__main__':
    main()
