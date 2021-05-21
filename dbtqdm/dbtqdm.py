from collections import Iterable
from io import StringIO, TextIOWrapper
from os import environ
from typing import Tuple, Union, Any
from datetime import datetime, timedelta
from tqdm import tqdm

from dbtqdm.args.server import DEF_DB_HOST, DEF_DB_PORT, DEF_DB_NAME
from dbtqdm.utils import format_interval

STATS_COLLECTION = '_stats_'


class EnvironError(Exception):
    pass


class MongoTqdm(tqdm):
    @property
    def bar_name(self) -> str:
        return self.__bar_name

    def __init__(self, iterable: Iterable = None, desc: str = None, total: float = None, leave: bool = True,
                 file: Union[TextIOWrapper, StringIO] = None, n_cols: int = None, min_interval: float = 0.1,
                 max_interval: float = 10.0, miniters: Union[int, float] = None, ascii: Union[bool, str] = None,
                 disable: bool = False, unit: str = 'it', unit_scale: Union[bool, int, float] = False,
                 dynamic_n_cols: bool = False, smoothing: float = 0.3, bar_format: str = None,
                 initial: Union[int, float] = 0, position: int = None, postfix: Union[dict, Any] = None,
                 unit_divisor: float = 1000, write_bytes: bool = None, lock_args: Tuple = None,
                 n_rows: int = None, colour: str = None, delay: float = 0, gui: bool = False, **kwargs) -> None:
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
           the environment variable TQDM_HOST. By default, localhost.
        :param port: Only for mode 'mongo'. The database port. If it is not set, this function will check if there is
           the environment variable TQDM_PORT. By default, 27017.
        :param replicaset: Only for mode 'mongo'. The database replicaset. If it is not set, this function will check if there is
           the environment variable TQDM_REPLICASET. By default, do not use it.
        :param bar_name: Only for mode 'mongo'. The bar progress name. If it is not set, this function will check if
           there is the environment variable TQDM_NAME. If it is not given, neither parameter o environment variable,
           then an exception is raised.

        :return:  decorated iterator.
        """
        self.__collection = None
        self.__mode = self.__db_property('mode', 'TQDM_MODE', False, 'auto')
        if self.__mode not in ['auto', 'mongo']:
            raise EnvironError(f'The environment variable TQDM_MODE cannot be "{self.__mode}". '
                               f'The available values are: "auto" or "mongo".')
        if self.__mode == 'mongo':
            host, port, replicaset, db_name, bar_name = self.__db_properties(**kwargs)
            if bar_name == STATS_COLLECTION:
                raise ValueError(f'The bar_name parameter cannot be the reserved collection "{STATS_COLLECTION}".')
            from pymongo import ASCENDING, DESCENDING
            from dbutils import connect_db

            self.__client = connect_db(host, port, replicaset)
            self.__db = self.__client[db_name]
            self.__stats = self.__db[STATS_COLLECTION]
            if 'stats_ix' not in self.__stats.index_information():
                self.__stats.create_index(
                    [('start_time', DESCENDING), ('bar_name', ASCENDING)], name='stats_ix', unique=True)
                self.__stats.create_index([('start_time', DESCENDING)], name='start_ix')
                self.__stats.create_index('bar_name', name='bar_ix')
            self.__collection = self.__db[bar_name]
            self.__bar_name = bar_name
            self.__start = datetime.timestamp(datetime.now())
        self.disable = disable
        for var in ['host', 'port', 'replicaset', 'db', 'name']:
            if var in kwargs:
                del kwargs[var]
        super(MongoTqdm, self).__init__(iterable=iterable, desc=desc, total=total, leave=leave, file=file,
                                        ncols=n_cols, mininterval=min_interval, maxinterval=max_interval,
                                        miniters=miniters, ascii=ascii, disable=disable, unit=unit,
                                        unit_scale=unit_scale, dynamic_ncols=dynamic_n_cols, smoothing=smoothing,
                                        bar_format=bar_format, initial=initial, position=position, postfix=postfix,
                                        unit_divisor=unit_divisor, write_bytes=write_bytes, lock_args=lock_args,
                                        nrows=n_rows, colour=colour, delay=delay, gui=gui, **kwargs)

    def __db_properties(self, **kwargs) -> Tuple[str, int, str, str, str]:
        try:
            host = self.__db_property('host', 'TQDM_HOST', default=DEF_DB_HOST, **kwargs)
            port = int(self.__db_property('port', 'TQDM_PORT', default=DEF_DB_PORT, **kwargs))
            replicaset = self.__db_property('replicaset', 'TQDM_REPLICASET', **kwargs)
            db_name = self.__db_property('db', 'TQDM_DB', default=DEF_DB_NAME, **kwargs)
            bar_name = self.__db_property('name', 'TQDM_NAME', required=True, **kwargs)
            return host, port, replicaset, db_name, bar_name
        except KeyError as e:
            raise EnvironError(f'To use the mode "mongo" for tqdm progress bar, '
                               f'it is necessary to define the following environment variable: {e.args[0]}')

    def display(self, msg: str = None, pos: int = None) -> bool:
        if self.__mode == 'auto':
            return super(MongoTqdm, self).display(msg, pos)
        self.format_dict['bar_name'] = self.bar_name
        self.format_dict['colour'] = self.colour
        return bool(self.__collection.replace_one({}, self.meter_dict(**self.format_dict), upsert=True))

    def close(self) -> None:
        if self.__mode == 'mongo' and self.__collection:
            collection, stats, start, bar_name = self.__collection, self.__stats, self.__start, self.__bar_name
            collection.drop()
            self.__collection = None
            meter = self.meter_dict(**self.format_dict)
            meter['bar_name'], meter['start_time'] = bar_name, start
            meter['end_time'] = datetime.timestamp(datetime.now())
            if bar_name:
                stats.replace_one({'start_time': start, 'bar_name': bar_name}, meter, upsert=True)

    @staticmethod
    def __db_property(var: str, env: str, required: bool = False, default: Any = None, **kwargs):
        return kwargs[var] if var in kwargs else environ[env] if required or env in environ else default

    @staticmethod
    def meter_dict(n: float, total: float, elapsed: float, prefix: str = '',
                   unit: str = 'it', unit_scale: Union[bool, int, float] = False, rate: str = None,
                   postfix: Any = '', unit_divisor: float = 1000, initial: float = 0,
                   colour: str = None, **extra_kwargs) -> dict:
        """  Return a string-based progress bar given some parameters

        :param n: Number of finished iterations.
        :param total: The expected total number of iterations. If meaningless (None),
            only basic progress statistics are displayed (no ETA).
        :param elapsed: Number of seconds passed since start.
        :param prefix: Prefix message (included in total width) [default: '']. Use as {desc} in bar_format string.
        :param unit: The iteration unit [default: 'it'].
        :param unit_scale: If 1 or True, the number of iterations will be printed with an appropriate SI metric prefix
            (k = 10^3, M = 10^6, etc.) [default: False]. If any other non-zero number, will scale `total` and `n`.
        :param rate: Manual override for iteration rate. If [default: None], uses n/elapsed.
        :param postfix: Similar to `prefix`, but placed at the end (e.g. for additional stats).
            Note: postfix is usually a string (not a dict) for this method,
            and will if possible be set to postfix = ', ' + postfix. However other types are supported (#382).
        :param unit_divisor: [default: 1000], ignored unless `unit_scale` is True.
        :param initial: The initial counter value [default: 0].
        :param colour: Bar colour (e.g. 'green', '#00ff00').

        :return: All dictionary with all the information about the meter, ready to do a representation display.
        """

        # sanity check: total
        total = None if total and n >= (total + 0.5) else total  # allow float imprecision (#849)

        # apply custom scale if necessary
        if unit_scale and unit_scale not in (True, 1):
            total = total * unit_scale if total else total
            n *= unit_scale
            rate = rate * unit_scale if rate else rate  # by default rate = self.avg_dn / self.avg_dt

        elapsed_str = format_interval(elapsed) if elapsed else '0s'

        # if unspecified, attempt to use rate = average speed
        # (we allow manual override since predicting time is an arcane art)
        rate = (n - initial) / elapsed if rate is None and elapsed else rate
        remaining = (total - n) / rate if rate and total else 0
        rate, primary_unit, secondary_unit = (1 / rate, 's', unit) if rate and rate <= 1 else (rate, unit, 's')
        remaining_str = format_interval(remaining) if rate else '?'
        percentage = 100 * n / total if total else 0
        postfix = postfix if postfix else ''
        try:
            eta = datetime.now() + timedelta(seconds=remaining) if rate and total else datetime.utcfromtimestamp(0)
        except OverflowError:
            eta = datetime.max

        return dict(
            n=n, total=total, unit=unit, primary_unit=primary_unit, secondary_unit=secondary_unit,
            unit_scale=unit_scale, unit_divisor=unit_divisor,
            rate=rate, elapsed=elapsed, elapsed_str=elapsed_str, remaining=remaining, remaining_str=remaining_str,
            eta=eta, percentage=percentage, desc=prefix + postfix, colour=colour, **extra_kwargs)
