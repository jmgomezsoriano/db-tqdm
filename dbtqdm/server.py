from os import environ

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from logging import getLogger
from importlib_resources import files

from monutils import connect_database
from mysutils.collections import del_keys
from pymongo import DESCENDING
from pymongo.database import Database

import dbtqdm
from dbtqdm.args.server import TqdmArgParser
from dbtqdm.consts import DEF_TITLE, DEF_INTERVAL, DEF_DB_PORT, DEF_HOST, DEF_PORT, DEF_DB_HOST, DEF_DB_NAME, \
    STATS_COLLECTION, DEF_ROOT_PATH

# root_path = environ['ROOT_PATH'] if 'ROOT_PATH' in environ else ''
app = FastAPI()
app.mount("/static", StaticFiles(directory=f'{files(dbtqdm)}/static'), name="static")
templates = Jinja2Templates(directory=f'{files(dbtqdm)}/templates')
logger = getLogger(__name__)
TQDM_ROUTE, BAR_ROUTE, STATS_ROUTE, REMOVE_ROUTE = '/api/tqdm', '/api/bar', '/api/stats', '/api/remove'
app.web_title, app.interval = DEF_TITLE, DEF_INTERVAL * 1000


@app.get('/', response_class=HTMLResponse)
def home(request: Request) -> templates.TemplateResponse:
    """ Show all the progress bar.
    :return: The home web page, which shows all the progress bars.
    """
    return templates.TemplateResponse("index.html",
                                      {'title': app.web_title, 'interval': app.interval, 'request': request})


@app.get(BAR_ROUTE + '/{bar_id}', response_class=HTMLResponse)
def bar_page(request: Request, bar_id: str) -> str:
    """ Show a bar.
    :param: The id of the bar to show. This id is formed by the bar name and bar name suffix.
    :return: The web page, which shows the specified progress bar.
    """
    return templates.get_template('bar.html').render(bar_name=bar_id, interval=app.interval, request=request)


@app.get('/health')
def health():
    """ Check if this service is alive. """
    return "I am ready!"


@app.get(TQDM_ROUTE + '/{bar_id}')
def tqdm(bar_id: str) -> dict:
    """ API to get the bar data give its id. If that progress bar is not active, then it will check the last finished
      progress bar with this id. If it does not exist, then return a error message.
    :param bar_id: The id of the progress bar. This id is formed by the bar name and bar name suffix.
    :return The progress bar information.
    :raise HTTPException: If the bar does not exist.
    """
    if bar_id in app.db.list_collection_names():
        return bar_progress(app.db, bar_id)

    obj = app.db[STATS_COLLECTION].find_one({'bar_id': bar_id}, sort=[('start', DESCENDING)])
    if obj:
        obj['remaining_str'] = '0s'
        obj['start_str'] = '0s'
        return del_keys(obj, '_id')
    raise HTTPException(404, f'Bar progress "{bar_id}" does not exist.')


@app.get(REMOVE_ROUTE + '/{bar_id}')
def remove(bar_id: str) -> bool:
    """ Remove a progress bar from the database. If the progress bar is still alive, then it will appear again
      in the next page updating.
    :param bar_id: The bar id to remove. This id is formed by the bar name and bar name suffix.
    :return: If the bar progress exists, then the bar information is returned, otherwise an error message is returned.
    :raise HTTPException: If the bar does not exist or it is already removed.
    """
    if bar_id in app.db.list_collection_names():
        app.db[bar_id].drop()
        return True
    raise HTTPException(404, f'Bar progress "{bar_id}" does not exist or it is already removed.')


@app.get(TQDM_ROUTE)
def all_tqdm() -> dict:
    """ Get the data of all the progress bars.
    :return: A dict with the page title and the data with all the progress bars.
    """
    return {
        'title': app.web_title,
        'bars': [bar_progress(app.db, name) for name in app.db.list_collection_names() if name != STATS_COLLECTION]
    }


def bar_progress(db: Database, bar_id: str) -> dict:
    """ Obtain the progress bar information from MongoDB from its id.
    :param db: The database.
    :param bar_id: The bar id to remove. This id is formed by the bar name and bar name suffix.
    :return: A dictionary with the progress bar information.
    """
    bar = db[bar_id].find_one({})
    if bar and '_id' in bar:
        del bar['_id']
    return bar


def start_server(title: str = DEF_TITLE, host: str = DEF_HOST, port: int = DEF_PORT,  root_path: str = DEF_ROOT_PATH,
                 db_host: str = DEF_DB_HOST, db_port: int = DEF_DB_PORT, replicaset: str = None,
                 db_name: str = DEF_DB_NAME, user: str = '', password: str = '',
                 cert_key_file: str = None, ca_file: str = None,
                 session_token: str = None, seconds_interval: int = DEF_INTERVAL * 1000) -> None:
    """ Start the server.
    :param title: The web page title.
    :param host: The web page host.
    :param port: The web page port.
    :param db_host: The database host.
    :param db_port: The database port.
    :param replicaset: The MongoDB replicaset.
    :param db_name: The database name.
    :param user: The database user.
    :param password: The user password.
    :param cert_key_file: The database cert key file.
    :param ca_file: The database CA file.
    :param session_token: The database session token.
    :param seconds_interval: The interval between the web page refreshing.
    """
    app.web_title, app.interval = title, seconds_interval
    logger.info(f'Starting the server with this parameters:\nHost: {host}\nPort: {port}\nRoot path: {root_path}\n'
                f'DB host: {db_host}\nDB port: {db_port}\nºReplicaset: {replicaset}\n')
    logger.info('Starting the server with this parameters:')
    app.db = connect_database(db_host, db_port, replicaset, db_name, user, password,
                              cert_key_file, ca_file, session_token)
    app.root_path = root_path
    uvicorn.run(app, host=host, port=port)


def main() -> None:
    """ The main function. """
    args = TqdmArgParser()
    start_server(args.title, args.host, args.port, args.root_path, args.db_host, args.db_port, args.replicaset, args.database,
                 args.user, args.password, args.cert_key_file, args.ca_file, args.session_token, args.interval)


if __name__ == '__main__':
    main()
