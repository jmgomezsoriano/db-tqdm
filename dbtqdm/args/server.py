from argparse import ArgumentParser

from dbtqdm.consts import DEF_HOST, DEF_PORT, DEF_DB_HOST, DEF_DB_PORT, DEF_DB_NAME, DEF_INTERVAL, DEF_TITLE


class TqdmArgParser(object):
    @property
    def title(self) -> str:
        return self._args.title

    @property
    def host(self) -> str:
        return self._args.host

    @property
    def port(self) -> int:
        return self._args.port

    @property
    def db_host(self) -> str:
        return self._args.db_host

    @property
    def db_port(self) -> int:
        return self._args.db_port

    @property
    def replicaset(self) -> str:
        return self._args.replicaset

    @property
    def database(self) -> str:
        return self._args.database

    @property
    def interval(self) -> int:
        return self._args.interval * 1000

    def __init__(self) -> None:
        parser = ArgumentParser(description='Start the server to serve the bar progress data.')
        self.set_arguments(parser)
        self._args = parser.parse_args()

    @staticmethod
    def set_arguments(parser: ArgumentParser) -> None:
        parser.add_argument('-H', '--host', type=str, metavar='HOST', default=DEF_HOST,
                            help=f'The server host. By default, {DEF_HOST}.')
        parser.add_argument('-p', '--port', type=int, metavar='PORT', default=DEF_PORT,
                            help=f'The server port. By default, {DEF_PORT}.')
        parser.add_argument('--db_host', type=str, metavar='HOST', default=DEF_DB_HOST,
                            help=f'The database host. By default, {DEF_HOST}.')
        parser.add_argument('--db_port', type=int, metavar='PORT', default=DEF_DB_PORT,
                            help=f'The database port. By default, {DEF_PORT}.')
        parser.add_argument('-r', '--replicaset', type=str, metavar='NAME',
                            help=f'The replicaset. By default, none.')
        parser.add_argument('-d', '--database', type=str, metavar='NAME', default=DEF_DB_NAME,
                            help=f'The database name. By default, {DEF_DB_NAME}.')
        parser.add_argument('-i', '--interval', type=int, metavar='SECONDS', default=DEF_INTERVAL,
                            help=f'The database name. By default, {DEF_DB_NAME}.')
        parser.add_argument('title', type=str, metavar='TITLE', default=DEF_TITLE, nargs='?',
                            help=f'The web page title. By default, "{DEF_TITLE}".')
