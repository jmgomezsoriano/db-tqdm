from typing import Union

from pymongo import MongoClient


def connect_db(host: str = 'localhost', port: int = 27017, replicaset: Union[str, None] = None) -> MongoClient:
    """ Connect with the database.
    :param host: The database connection host.
    :param port: The database connection port.
    :param replicaset: The replicaset. If None, then, replicaset is not used.
    :return: The MongoDB client.
    """
    return MongoClient(host, port, replicaset=replicaset) if replicaset else MongoClient(host, port)
