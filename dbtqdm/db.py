from abc import ABC, ABCMeta, abstractmethod
from io import TextIOWrapper, StringIO
from typing import Iterable, Union, Any, Tuple
from os import environ
from datetime import datetime, timedelta

from tqdm.auto import tqdm

from dbtqdm.consts import DEF_DB_NAME
from dbtqdm.utils import format_interval


class EnvironError(Exception):
    pass


class DatabaseTqdm(tqdm, ABC):
    """ Class to create a TQDM process bar based on MongoDB. """
    __metaclass__ = ABCMeta

    @property
    def mode(self) -> str:
        """
        :return: The TQDM mode. 'normla' for normal tqdm normal mode or 'mongo' to use MongoDB database.
        """
        return self._mode

    @property
    def database(self) -> str:
        """
        :return: The database name for any database mode.
        """
        return self._database

    @property
    def bar_name(self) -> str:
        """
        :return: The bar progress name for any database mode.
        """
        return self._bar_name

    @property
    def suffix(self) -> str:
        """
        :return: The suffix to build the bar id from the bar name. It will value bar_name + suffix.
        """
        return self._suffix

    @property
    def bar_id(self) -> str:
        """
        :return: The bar progress id. It will formed with bar_name + suffix.
        """
        return self.bar_name + self.suffix

    @property
    def start(self) -> float:
        """
        :return: Timestamp when the bar progress started.
        """
        return self._start

    def __init__(self, iterable: Iterable = None, desc: str = None, total: float = None, leave: bool = True,
                 file: Union[TextIOWrapper, StringIO] = None, n_cols: int = None, min_interval: float = 0.1,
                 max_interval: float = 10.0, miniters: Union[int, float] = None, ascii: Union[bool, str] = None,
                 disable: bool = False, unit: str = 'it', unit_scale: Union[bool, int, float] = False,
                 dynamic_n_cols: bool = False, smoothing: float = 0.3, bar_format: str = None,
                 initial: Union[int, float] = 0, position: int = None, postfix: Union[dict, Any] = None,
                 unit_divisor: float = 1000, write_bytes: bool = None, lock_args: Tuple = None,
                 n_rows: int = None, colour: str = None, delay: float = 0, gui: bool = False,
                 mode: str = 'normal', database: str = 'tqdm', name: str = None, suffix: str = None, **kwargs) -> None:
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
        :param mode: Two modes: normal (normal tqdm behavior), or mongo (using MongoDB as bar progress).
            If it is not set, this function will check if there is the environment variable TQDM_MODE. By default, auto.
        :param database: The database name. By default, tqdm.
        :param bar_name: Only for mode 'mongo'. The bar progress name. If it is not set, this function will check if
           there is the environment variable TQDM_NAME. If it is not given, neither parameter o environment variable,
           then an exception is raised.
        :param suffix: Only for mode 'mongo'. If it is set, the name is form concatenating the bar name with this suffix
           (name + suffix). This method will use when the bar name is given by environment variable instead of
           constructor parameter, in order to have several bar progress for the same name.

        :return:  decorated iterator.
        """
        self._mode = self._db_property('mode', mode, 'TQDM_MODE', False, 'normal')
        if self._mode not in ['normal', 'mongo']:
            raise EnvironError(f'The environment variable TQDM_MODE cannot be "{self._mode}". '
                               f'The available values are: "normal" or "mongo".')
        if self.mode == 'mongo':
            try:
                self._database = self._db_property('db', database, 'TQDM_DB_NAME', default=DEF_DB_NAME)
                self._bar_name = self._db_property('name', name, 'TQDM_NAME', required=True)
                self._suffix = self._db_property('suffix', suffix, 'TQDM_SUFFIX', default='')
            except KeyError as e:
                raise EnvironError(f'To use the mode "{self.__name__}" for tqdm progress bar, '
                                   f'it is necessary to define the following environment variable: {e.args[0]}')
        self._start = datetime.timestamp(datetime.now())
        super(DatabaseTqdm, self).__init__(iterable=iterable, desc=desc, total=total, leave=leave, file=file,
                                           ncols=n_cols, mininterval=min_interval, maxinterval=max_interval,
                                           miniters=miniters, ascii=ascii, disable=disable, unit=unit,
                                           unit_scale=unit_scale, dynamic_ncols=dynamic_n_cols, smoothing=smoothing,
                                           bar_format=bar_format, initial=initial, position=position, postfix=postfix,
                                           unit_divisor=unit_divisor, write_bytes=write_bytes, lock_args=lock_args,
                                           nrows=n_rows, colour=colour, delay=delay, gui=gui, **kwargs)

    def close(self) -> None:
        """ Close the TQDM bar progress. """
        if self._mode == 'mongo':
            bar_name, suffix, start = self.bar_name, self.suffix, self._start
            meter = self.meter_dict(**self.format_dict)
            meter['bar_name'], meter['suffix'], meter['start_time'] = bar_name, suffix, start
            meter['start_time_str'] = datetime.utcfromtimestamp(start)
            meter['end_time'] = datetime.timestamp(datetime.now())
            meter['end_time_str'] = datetime.utcfromtimestamp(datetime.timestamp(datetime.now()))
            meter['finished'] = True
            meter['bar_id'] = self.bar_id
            self.close_bar(meter)
        super(DatabaseTqdm, self).close()

    @abstractmethod
    def close_bar(self, bar: dict) -> None:
        """ Send the message to the class children to close the bar.
        :param bar: The bar information.
        """
        pass

    def display(self, msg: str = None, pos: int = None, **kwargs) -> bool:
        """ Display the TQDM bar progress. If the mode is 'normal', it will be displayed as usual.
          If not, it will update the database information with the new values of the bar progress.

        :param msg: The bar message.
        :param pos: The current progress bar position.
        :return: True if anything was well, otherwise an exception is raised.
        """
        if self._mode == 'normal':
            return super(DatabaseTqdm, self).display(msg, pos, **kwargs)
        self.format_dict['bar_name'] = self.bar_name
        self.format_dict['suffix'] = self.suffix
        self.format_dict['colour'] = self.colour
        self.save_changes()
        return True

    @abstractmethod
    def save_changes(self) -> None:
        """ Save changes of the bar progress in the database. """
        pass

    @staticmethod
    def _db_property(param_name: str, param_value: Any, env: str, required: bool = False, default: Any = None) -> Any:
        """ Get a property value if it exists either in the kwargs argument or in the environment variables.
        :param param_value: The variable name.
        :param env: The environment variable name.
        :param required: True if that variable is required, otherwise False.
        :param default: The default value when the variable is not required and it does not exist.
        :return: The variable value.
        :raise KeyError: If the variable does not exist.
        """
        if env in environ:
            return environ[env]
        if param_value is None and required:
            raise ValueError(f'The parameter "{param_name}" is required for the current TQDM mode, however, neither, '
                             f'it have no value, nor it is not defined in the environment variable "{env}".')
        return default if param_value is None else param_value

    def meter_dict(self, n: float, total: float, elapsed: float, prefix: str = '',
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
            n=n, initial=initial, total=total, unit=unit, primary_unit=primary_unit, secondary_unit=secondary_unit,
            unit_scale=unit_scale, unit_divisor=unit_divisor,
            rate=rate, elapsed=elapsed, elapsed_str=elapsed_str, remaining=remaining, remaining_str=remaining_str,
            eta=eta, percentage=percentage, desc=prefix + postfix, colour=colour,
            bar_name=self.bar_name, suffix=self.suffix, start=self._start, finished=False,
            start_time_str=datetime.utcfromtimestamp(self._start), **extra_kwargs)
