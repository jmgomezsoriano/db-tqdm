import os
from typing import Union
from urllib.parse import urlparse
from importlib_resources import files

PAGES_MODULE = 'dbtqdm.templates'


def request_base(request, service: str = '') -> str:
    """
    Obtain the final URL to the service dynamically from a request.

    :param request: The request to obtain the URL.
    :param service: The path to the servies to join with the request base.
    :return: A string with the URL.
    """
    uri = urlparse(request.base_url)
    path = request.environ['HTTP_X_ENVOY_ORIGINAL_PATH'] if 'HTTP_X_ENVOY_ORIGINAL_PATH' in request.environ else ''
    if path.endswith('/') and service.startswith('/'):
        path += service[1:]
    elif not path.endswith('/') and not service.startswith('/'):
        path += '/' + service
    else:
        path += service
    return f'{uri.scheme}://{uri.hostname}' + (f':{uri.port}' if uri.port else '') + f'{path}'


def time2date(t: float) -> (int, int, int, int, int):
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


def format_date(w: int, d: int, h: int, m: int, s: int):
    return (f'{w}w ' if w else '') + \
           (f'{d}d ' if d else '') + \
           (f'{h}h ' if h else '') + \
           (f'{m}m ' if m else '') + \
           (f'{s}s' if s else '')


def format_interval(interval: float) -> str:
    return format_date(*time2date(interval))


def get_page_path(file: str) -> Union[str, None]:
    """ Get a resource path from data folder of the installation library in production environment or the data folder
      in development environment.

    :param file: The file name to get its path.
    :return: The absolute path to the file.
    """
    # Try to find this file in the module installation directory.
    file_path = files(PAGES_MODULE).joinpath(file)
    if os.path.exists(file_path):
        return str(file_path)
    # If not, it is supposed that are you working in develop environment, then return the path to that files
    file_path = os.path.join(*(PAGES_MODULE.split('.') + [file]))
    if os.path.exists(file_path):
        return file_path
    return None
