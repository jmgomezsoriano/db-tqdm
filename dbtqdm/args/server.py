from argparse import ArgumentParser
from os import environ

from dbtqdm.consts import DEF_HOST, DEF_PORT, DEF_DB_HOST, DEF_DB_PORT, DEF_DB_NAME, DEF_INTERVAL, DEF_TITLE, \
    DEF_DB_TYPE, DB_TYPES


class TqdmArgParser(object):
    """ Argument parser for the server. """
    @property
    def title(self) -> str:
        """
        :return: The web title. By default, "Process monitors".
        """
        return self._args.title

    @property
    def host(self) -> str:
        """
        :return: The server host. By default, "localhost".
        """
        return self._args.host

    @property
    def port(self) -> int:
        """
        :return: The server port. By default, 5000.
        """
        return self._args.port

    @property
    def db_type(self) -> str:
        """
        :return: The database manager type. By default, "mongo". At the moment only mongo is available.
        """
        return self._args.db_type

    @property
    def db_host(self) -> str:
        """
        :return: The database host. By default, "localhost".
        """
        return self._args.db_host

    @property
    def db_port(self) -> int:
        """
        :return: The database port. By default, 27017.
        """
        return self._args.db_port

    @property
    def replicaset(self) -> str:
        """
        :return: The MongoDB replicaset. By default, it is not used.
        """
        return self._args.replicaset

    @property
    def database(self) -> str:
        """
        :return: The database name. By default, "tqdm".
        """
        return self._args.database

    @property
    def user(self) -> str:
        """
        :return: The database name. By default, "tqdm".
        """
        return self._args.user

    @property
    def password(self) -> str:
        """
        :return: The database name. By default, "tqdm".
        """
        return self._args.password

    @property
    def cert_key_file(self) -> str:
        """
        :return: The database name. By default, "tqdm".
        """
        return self._args.cert_key_file

    @property
    def ca_file(self) -> str:
        """
        :return: The database name. By default, "tqdm".
        """
        return self._args.ca_file

    @property
    def session_token(self) -> str:
        """
        :return: The database name. By default, "tqdm".
        """
        return self._args.session_token

    @property
    def interval(self) -> int:
        """
        :return: The interval between page refreshing to update the process bars. By default, 5 (seconds).
        """
        return self._args.interval * 1000

    def __init__(self) -> None:
        """ Constructor. """
        parser = ArgumentParser(description='Start the server to serve the bar progress data.')
        self.set_arguments(parser)
        self._args = parser.parse_args()

    @staticmethod
    def set_arguments(parser: ArgumentParser) -> None:
        """ Set the parser arguments.
        :parser parser: The parser to add the arguments.
        """
        host = environ.get('TQDM_HOST', DEF_HOST)
        port = environ.get('TQDM_PORT',DEF_PORT)
        db_type = environ.get('TQDM_TYPE', DEF_DB_TYPE)
        db_host = environ.get('TQDM_DB_HOST', DEF_DB_HOST)
        db_port = environ.get('TQDM_DB_PORT', DEF_DB_PORT)
        replicaset = environ.get('TQDM_REPLICASET')
        db_name = environ.get('TQDM_DB_NAME', DEF_DB_NAME)
        db_user = environ.get('TQDM_DB_USER')
        db_password = environ.get('TQDM_DB_PASSWORD')
        cert_key_file = environ.get('TQDM_CERT_KEY_FILE')
        ca_file = environ.get('TQDM_CA_FILE')
        session_token = environ.get('TQDM_SESSION_TOKEN')
        interval = environ.get('TQDM_INTERVAL', DEF_INTERVAL)
        title = environ.get('TQDM_TITLE', DEF_TITLE)

        parser.add_argument('-H', '--host', type=str, metavar='HOST', default=host,
                            help=f'The server host. By default, {host}.')
        parser.add_argument('-P', '--port', type=int, metavar='PORT', default=port,
                            help=f'The server port. By default, {port}.')
        parser.add_argument('-t', '--db_type', type=str.lower, metavar='TYPE', default=db_type, choices=DB_TYPES,
                            help=f'The database host. By default, {db_type}. Available databases: {DB_TYPES}.')
        parser.add_argument('--db_host', type=str, metavar='HOST', default=db_host,
                            help=f'The database host. By default, {db_host}.')
        parser.add_argument('--db_port', type=int, metavar='PORT', default=db_port,
                            help=f'The database port. By default, {db_port}.')
        parser.add_argument('-r', '--replicaset', type=str, metavar='NAME', default=replicaset,
                            help=f'The replicaset. By default, none.')
        parser.add_argument('-d', '--database', type=str, metavar='NAME', default=db_name,
                            help=f'The database name. By default, {db_name}.')
        parser.add_argument('-u', '--user', type=str, metavar='USER', default=db_user,
                            help=f'The database user. By default, none.')
        parser.add_argument('-p', '--password', type=str, metavar='PASS', default=db_password,
                            help=f'The user password. By default, none.')
        parser.add_argument('--cert_key_file', type=str, metavar='FILE', default=cert_key_file,
                            help=f'The cert key fle to connect to the database. By default, none.')
        parser.add_argument('--ca_file', type=str, metavar='FILE', default=ca_file,
                            help=f'The CA file to connect to the database. By default, none.')
        parser.add_argument('--session_token', type=str, metavar='SESSION', default=session_token,
                            help=f'The session token to connect to the database. By default, none.')
        parser.add_argument('-i', '--interval', type=int, metavar='SECONDS', default=interval,
                            help=f'The default web refresh interval. By default, {interval}.')
        parser.add_argument('title', type=str, metavar='TITLE', default=title, nargs='?',
                            help=f'The web page title. By default, "{title}".')
