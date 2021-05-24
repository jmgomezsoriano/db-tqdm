from typing import Tuple, Union

from flask import Flask, render_template, json, jsonify, Response
from flask_cors import CORS
from logging import getLogger

from pymongo import DESCENDING
from pymongo.database import Database

from dbtqdm.mongo import connect_db
from dbtqdm.args.server import TqdmArgParser
from dbtqdm.consts import DEF_TITLE, DEF_INTERVAL, DEF_DB_PORT, DEF_HOST, DEF_PORT, DEF_DB_HOST, DEF_DB_NAME, \
    STATS_COLLECTION

app = Flask(__name__, template_folder='templates')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
logger = getLogger(__name__)
TQDM_ROUTE, BAR_ROUTE, STATS_ROUTE, REMOVE_ROUTE = '/tqdm', '/bar', '/stats', '/remove'
web_title, interval = DEF_TITLE, DEF_INTERVAL * 1000


@app.route('/')
def home() -> str:
    """ Show all the progress bar.
    :return: The home web page, which shows all the progress bars.
    """
    global web_title, interval
    return render_template('index.html', title=web_title, interval=interval)


@app.route(BAR_ROUTE + '/<bar_id>')
def bar_page(bar_id: str) -> str:
    """ Show a bar.
    :param: The id of the bar to show. This id is formed by the bar name and bar name suffix.
    :return: The web page, which shows the specified progress bar.
    """
    global web_title, interval
    return render_template('bar.html', bar_name=bar_id, interval=interval)


@app.route('/health')
def health():
    """ Check if this service is alive. """
    return "I am ready!"


@app.route(TQDM_ROUTE + '/<bar_id>', methods=['GET'])
def tqdm(bar_id: str) -> Union[dict, Tuple[Response, int]]:
    """ API to get the bar data give its id. If that progress bar is not active, then it will check the last finished
      progress bar with this id. If it does not exist, then return a error message.
    :param bar_id: The id of the progress bar. This id is formed by the bar name and bar name suffix.
    """
    global db
    if bar_id in db.list_collection_names():
        return bar_progress(db, bar_id)

    obj = db[STATS_COLLECTION].find_one({'bar_id': bar_id}, sort=[('start', DESCENDING)])
    if obj:
        del obj['_id']
        obj['remaining_str'] = '0s'
        obj['start_str'] = '0s'
        return obj
    return jsonify(error=str(f'Bar progress "{bar_id}" does not exist.')), 404


@app.route(REMOVE_ROUTE + '/<bar_id>', methods=['GET'])
def remove(bar_id: str) -> Union[str, Tuple[Response, int]]:
    """ Remove a progress bar from the database. If the progress bar is still alive, then it will appear again
      in the next page updating.
    :param bar_id: The bar id to remove. This id is formed by the bar name and bar name suffix.
    :return: If the bar progress exists, then the bar information is returned, otherwise an error message is returned.
    """
    global db
    if bar_id in db.list_collection_names():
        db[bar_id].drop()
        return json.dumps(True)
    return jsonify(error=str(f'Bar progress "{bar_id}" does not exist or it is already removed.')), 404


@app.route(TQDM_ROUTE, methods=['GET'])
def all_tqdm() -> dict:
    """ Get the data of all the progress bars.
    :return: A dict with the page title and the data with all the progress bars.
    """
    global db, web_title
    return {
        'title': web_title,
        'bars': [bar_progress(db, name) for name in db.list_collection_names() if name != STATS_COLLECTION]
    }


def bar_progress(db: Database, bar_id: str) -> dict:
    """ Obtain the progress bar information from MongoDB from its id.
    :param db: The database.
    :param bar_id: The bar id to remove. This id is formed by the bar name and bar name suffix.
    :return: The
    """
    bar = db[bar_id].find_one({})
    if bar and '_id' in bar:
        del bar['_id']
    return bar


def start_server(title: str = DEF_TITLE, host: str = DEF_HOST, port: int = DEF_PORT,  db_host: str = DEF_DB_HOST,
                 db_port: int = DEF_DB_PORT, replicaset: str = None, db_name: str = DEF_DB_NAME,
                 seconds_interval: int = DEF_INTERVAL * 1000) -> None:
    """ Start the server.
    :param title: The web page title.
    :param host: The web page host.
    :param port: The web page port.
    :param db_host: The database host.
    :param db_port: The database port.
    :param replicaset: The MongoDB replicaset.
    :param db_name: The database name.
    :param seconds_interval: The interval between the web page refreshing.
    """
    global db, web_title, interval
    web_title, interval = title, seconds_interval
    client = connect_db(db_host, db_port, replicaset)
    db = client[db_name]
    app.run(host, port)


def main() -> None:
    """ The main function. """
    args = TqdmArgParser()
    start_server(args.title, args.host, args.port, args.db_host, args.db_port, args.replicaset, args.database,
                 args.interval)


if __name__ == '__main__':
    main()
