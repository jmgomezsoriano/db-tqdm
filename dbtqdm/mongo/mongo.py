import logging
from collections import Iterable
from io import StringIO, TextIOWrapper
from typing import Tuple, Union, Any

from dbtqdm import DatabaseTqdm
from dbtqdm.consts import STATS_COLLECTION, DEF_DB_HOST, DEF_DB_PORT, DEF_DB_NAME
from dbtqdm.db import EnvironError

logger = logging.getLogger(__name__)


class MongoTqdm(DatabaseTqdm):
    """ Class to create a TQDM process bar based on MongoDB. """
    def __init__(self, iterable: Iterable = None, desc: str = None, total: float = None, leave: bool = True,
                 file: Union[TextIOWrapper, StringIO] = None, n_cols: int = None, min_interval: float = 0.1,
                 max_interval: float = 10.0, miniters: Union[int, float] = None, ascii: Union[bool, str] = None,
                 disable: bool = False, unit: str = 'it', unit_scale: Union[bool, int, float] = False,
                 dynamic_n_cols: bool = False, smoothing: float = 0.3, bar_format: str = None,
                 initial: Union[int, float] = 0, position: int = None, postfix: Union[dict, Any] = None,
                 unit_divisor: float = 1000, write_bytes: bool = None, lock_args: Tuple = None,
                 n_rows: int = None, colour: str = None, delay: float = 0, gui: bool = False,
                 mode: str = 'normal', database: str = 'tqdm', name: str = None, suffix: str = None,
                 host: str = None, port: int = None, replicaset: str = None, user: str = None, password: str = None,
                 cert_key_file: str = None, ca_file: str = None, session_token: str = None, **kwargs) -> None:
        """
        :param iterable: Iterable to decorate with a progressbar. Leave blank to manually manage the updates.
        :param desc: Prefix for the progressbar.
        :param total: The number of expected iterations. If unspecified, len(iterable) is used if possible.
           If float("inf") or as a last resort, only basic progress statistics are displayed (no ETA, no progressbar).
           If `gui` is True and this parameter needs subsequent updating, specify an initial arbitrary large positive
           number, e.g. 9e9.
        :param leave: If [default: True], keeps all traces of the progressbar upon termination of iteration.
           If `None`, will leave only if `position` is `0`.
        :param file: Specifies where to output the progress messages (default: sys.stderr).
           Uses `file.write(str)` and `file.flush()` methods.  For encoding, see `write_bytes`.
        :param n_cols: The width of the entire output message. If specified, dynamically resizes the progressbar to stay
           within this bound. If unspecified, attempts to use environment width. The fallback is a meter width of 10 and
           no limit for the counter and statistics. If 0, will not print any meter (only stats).
        :param min_interval: Minimum progress display update interval [default: 0.1] seconds.
        :param max_interval: Maximum progress display update interval [default: 10] seconds. Automatically adjusts
           `miniters` to correspond to `min_interval` after long display update lag. Only works if `dynamic_miniters`
           or monitor thread is enabled.
        :param miniters: Minimum progress display update interval, in iterations. If 0 and `dynamic_miniters`,
           will automatically adjust to equal `mininterval` (more CPU efficient, good for tight loops).
           If > 0, will skip display of specified number of iterations.
           Tweak this and `mininterval` to get very efficient loops. If your progress is erratic with both fast and slow
           iterations (network, skipping items, etc) you should set miniters=1.
        :param ascii: If unspecified or False, use unicode (smooth blocks) to fill the meter.
           The fallback is to use ASCII characters " 123456789#".
        :param disable: Whether to disable the entire progressbar wrapper [default: False].
           If set to None, disable on non-TTY.
        :param unit: String that will be used to define the unit of each iteration [default: it].
        :param unit_scale: If 1 or True, the number of iterations will be reduced/scaled automatically and a metric
           prefix following the International System of Units standard will be added (kilo, mega, etc.)
           [default: False]. If any other non-zero number, will scale `total` and `n`.
        :param dynamic_n_cols: If set, constantly alters `ncols` and `nrows` to the environment
           (allowing for window resizes) [default: False].
        :param smoothing: Exponential moving average smoothing factor for speed estimates (ignored in GUI mode).
           Ranges from 0 (average speed) to 1 (current/instantaneous speed) [default: 0.3].
        :param bar_format: Specify a custom bar string formatting. May impact performance.
           [default: '{l_bar}{bar}{r_bar}'], where l_bar='{desc}: {percentage:3.0f}%|' and
           r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
           Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt, percentage, elapsed, elapsed_s, ncols, nrows,
           desc, unit, rate, rate_fmt, rate_noinv, rate_noinv_fmt, rate_inv, rate_inv_fmt, postfix, unit_divisor,
           remaining, remaining_s, eta.
           Note that a trailing ": " is automatically removed after {desc} if the latter is empty.
        :param initial: The initial counter value. Useful when restarting a progress bar [default: 0].
           If using float, consider specifying `{n:.3f}` or similar in `bar_format`, or specifying `unit_scale`.
        :param position: Specify the line offset to print this bar (starting from 0). Automatic if unspecified.
           Useful to manage multiple bars at once (eg, from threads).
        :param postfix: Specify additional stats to display at the end of the bar.
           Calls `set_postfix(**postfix)` if possible (dict).
        :param unit_divisor: [default: 1000], ignored unless `unit_scale` is True.
        :param write_bytes: If (default: None) and `file` is unspecified, bytes will be written in Python 2.
            If `True` will also write bytes. In all other cases will default to unicode.
        :param lock_args: Passed to `refresh` for intermediate output (initialisation, iterating, and updating).
        :param n_rows: The screen height. If specified, hides nested bars outside this bound.
            If unspecified, attempts to use environment height. The fallback is 20.
        :param colour: Bar colour (e.g. 'green', '#00ff00').
        :param delay: Don't display until [default: 0] seconds have elapsed.
        :param gui: WARNING: internal parameter - do not use. Use tqdm.gui.tqdm(...) instead.
            If set, will attempt to use matplotlib animations for a graphical output [default: False].
        :param mode: Two modes: auto (normal tqdm behavior), or mongo (using MongoDB as bar progress).
            If it is not set, this function will check if there is the environment variable TQDM_MODE. By default, auto.
        :param host: Only for mode 'mongo'. The database host. If it is not set, this function will check if there is
           the environment variable TQDM_DB_HOST. By default, localhost.
        :param port: Only for mode 'mongo'. The database port. If it is not set, this function will check if there is
           the environment variable TQDM_DB_PORT. By default, 27017.
        :param replicaset: Only for mode 'mongo'. The database replicaset. If it is not set, this function will check
           if there is the environment variable TQDM_DB_REPLICASET. By default, do not use it.
        :param database: The database name. By default, tqdm.  If it is not set, this function will check
           if there is the environment variable TQDM_DB_NAME. By default, "tqdm".
        :param bar_name: Only for mode 'mongo'. The bar progress name. If it is not set, this function will check if
           there is the environment variable TQDM_NAME. If it is not given, neither parameter o environment variable,
           then an exception is raised.
        :param suffix: Only for mode 'mongo'. If it is set, the name is form concatenating the bar name with this suffix
           (name + suffix). This method will use when the bar name is given by environment variable instead of
           constructor parameter, in order to have several bar progress for the same name.

        :return:  decorated iterator.
        """
        self.__collection = None
        self._mode = self._db_property('mode', mode, 'TQDM_MODE', False, 'normal')
        if self._mode == 'mongo':
            host = self._db_property('host', host, 'TQDM_DB_HOST', default=DEF_DB_HOST)
            port = int(self._db_property('port', port, 'TQDM_DB_PORT', default=DEF_DB_PORT))
            replicaset = self._db_property('replicaset', replicaset, 'TQDM_DB_REPLICASET')
            database = self._db_property('db', database, 'TQDM_DB_NAME', default=DEF_DB_NAME)
            user = self._db_property('db', user, 'TQDM_DB_USER', default='')
            password = self._db_property('db', password, 'TQDM_DB_PASSWORD', default='')
            bar_name = self._db_property('name', name, 'TQDM_NAME', required=True)
            suffix = self._db_property('suffix', suffix, 'TQDM_SUFFIX', default='')
            cert_key_file = self._db_property('suffix', cert_key_file, 'TQDM_DB_CERT_KEY_FILE', default=None)
            ca_file = self._db_property('suffix', ca_file, 'TQDM_DB_CA_FILE', default=None)
            session_token = self._db_property('suffix', session_token, 'TQDM_DB_SESSION_TOKEN', default=None)
            self._database, self._bar_name, self._suffix = database, bar_name, suffix
            if self.bar_name == STATS_COLLECTION:
                raise ValueError(f'The bar_name parameter cannot be the reserved collection "{STATS_COLLECTION}".')
            try:
                from monutils import connect
                from pymongo import ASCENDING, DESCENDING
                from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, ConfigurationError
                try:
                    self.__client = connect(host, port, replicaset, user, password, cert_key_file, ca_file, session_token)
                    self.__db = self.__client[database]
                    self.__stats = self.__db[STATS_COLLECTION]
                    if 'stats_ix' not in self.__stats.index_information():
                        self.__stats.create_index(
                            [
                                ('start_time', DESCENDING),
                                ('bar_ix', ASCENDING)
                            ],
                            name='stats_ix', unique=True)
                        self.__stats.create_index([('start_time', DESCENDING)], name='start_ix')
                        self.__stats.create_index('bar_id', name='bar_ix')

                    self.__collection = self.__db[self.bar_id]
                except (ServerSelectionTimeoutError, OperationFailure, ConfigurationError) as e:
                    logger.warning(f'The connexion to the MongoDB database has not been done: {str(e)}.')
                    self._mode = 'normal'
            except ImportError as e:
                logger.warning('The monutils module is required, please, install:\n\npip install monutils>=0.1.3,<2.0')
                self._mode = 'normal'

        self.disable = disable
        super(MongoTqdm, self).__init__(iterable=iterable, desc=desc, total=total, leave=leave, file=file,
                                        n_cols=n_cols, min_interval=min_interval, max_interval=max_interval,
                                        miniters=miniters, ascii=ascii, disable=disable, unit=unit,
                                        unit_scale=unit_scale, dynamic_n_cols=dynamic_n_cols, smoothing=smoothing,
                                        bar_format=bar_format, initial=initial, position=position, postfix=postfix,
                                        unit_divisor=unit_divisor, write_bytes=write_bytes, lock_args=lock_args,
                                        n_rows=n_rows, colour=colour, delay=delay, gui=gui,
                                        mode=self.mode, database=database, name=name, suffix=suffix, **kwargs)

    def __db_properties(self, **kwargs) -> Tuple[str, int, str, str, str, str]:
        """ Get the database connection parameters from the kwargs if they are defined or
          from the environment variables.
        :param kwargs: The extra parameters to connect with the database.
        :return: A tuple with the host, port, replicaset, database name, progress bar name and suffix.
        :raise EnvironError: If the necessary parameters are not defined neither the kwargs parameter nor
          environ variables.
        """
        try:
            host = self._db_property('host', 'TQDM_DB_HOST', default=DEF_DB_HOST, **kwargs)
            port = int(self._db_property('port', 'TQDM_DB_PORT', default=DEF_DB_PORT, **kwargs))
            replicaset = self._db_property('replicaset', 'TQDM_DB_REPLICASET', **kwargs)
            database = self._db_property('db', 'TQDM_DB_NAME', default=DEF_DB_NAME, **kwargs)
            bar_name = self._db_property('name', 'TQDM_NAME', required=True, **kwargs)
            suffix = self._db_property('suffix', 'TQDM_SUFFIX', default='', **kwargs)
            return host, port, replicaset, database, bar_name, suffix
        except KeyError as e:
            raise EnvironError(f'To use the mode "mongo" for tqdm progress bar, '
                               f'it is necessary to define the following environment variable: {e.args[0]}')

    def save_changes(self):
        """ Save the current data of the progress bar into MongoDB. """
        if not self.__collection:
            return False
        return bool(self.__collection.replace_one({}, self.meter_dict(**self.format_dict), upsert=True))

    def close_bar(self, bar: dict) -> None:
        """ The  final action when the progress bar is finished.
          Usually, it stores the data into a history table or collection.
        :param bar: The progress bar information.
        """
        if self.__collection:
            bar_name, suffix, start = self.bar_name, self.suffix, self.start
            collection, stats = self.__collection, self.__stats
            collection.drop()
            self.__collection = None
            if bar_name:
                stats.replace_one({'start_time': start, 'bar_name': bar_name, 'suffix': suffix}, bar, upsert=True)
