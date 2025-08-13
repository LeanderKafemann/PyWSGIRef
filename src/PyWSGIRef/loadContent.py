"""
Content loading helper.
"""
import requests

from .exceptions import *
from .finished import finished

def loadFromWeb(url: str) -> str:
    """
    Loads content from the given URL with the given data.
    """
    if finished.value:
        raise ServerAlreadyGeneratedError()
    if not url.endswith(".pyhtml"):
        raise InvalidFiletypeError()

    # trick GitHub Pages guardian
    headers = {"User-Agent": "Mozilla/5.0", "realAccessDeviceMonitorAgent": "PyWSGIRef/1.1"}
    rq = requests.get(url, headers=headers)
    if rq.status_code != 200:
        raise AccessToTemplateForbidden()
    rq_content = rq.content
    return rq_content.decode()

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