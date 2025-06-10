"""
Content loading helper.
"""
import requests

from .exceptions import *
from .finished import finished

def loadFromWeb(url: str, data: dict = {}) -> str:
    """
    Loads content from the given URL with the given data.
    """
    if finished.value:
        raise ServerAlreadyGeneratedError()
    if not url.endswith(".pyhtml"):
        raise InvalidFiletypeError()
    rq = requests.post(url, data).content
    return rq.decode()

def loadFromFile(filename: str) -> str:
    """
    Loads a file from the given filename.
    """
    if finished.value:
        raise ServerAlreadyGeneratedError()
    if not filename.endswith(".pyhtml"):
        raise InvalidFiletypeError()
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    return content