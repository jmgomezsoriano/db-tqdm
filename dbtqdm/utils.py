from typing import Tuple


def split_interval(t: float) -> Tuple[int, int, int, int, int]:
    """ Split an interval of time into weeks, days, hours, minutes, and seconds.
    :param t: The time interval to split.
    :return: A tuple with the number of weeks, days, hours, minutes, and seconds.
    """
    seconds = round(t)
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    days = hours // 24
    hours = hours % 24
    weeks = days // 7
    days = days % 7
    return weeks, days, hours, minutes, seconds


def interval2str(w: int, d: int, h: int, m: int, s: int):
    """ Convert splited weeks, days, hours, minutes, and seconds into a string.
    :param w: The number of weeks.
    :param d: The number of days.
    :param h: The number of hours.
    :param m: The number of minutes.
    :param s: The number of seconds.
    :return: The formatted interval in this format: ?w ?d ?h ?m ?s. Where w are weeks, d are days, m are minutes,
       and s are seconds
    """
    return (f'{w}w ' if w else '') + \
           (f'{d}d ' if d else '') + \
           (f'{h}h ' if h else '') + \
           (f'{m}m ' if m else '') + \
           (f'{s}s' if s else '')


def format_interval(interval: float) -> str:
    """ Format an interval of time.
    :param interval: The interval of time to format.
    :return: The formatted interval in this format: ?w ?d ?h ?m ?s. Where w are weeks, d are days, m are minutes,
       and s are seconds
    """
    return interval2str(*split_interval(interval))
