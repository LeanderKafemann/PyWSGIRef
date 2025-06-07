"""
PYWSGIREF
"""
from typing import Callable
import requests
from wsgiref.simple_server import make_server, WSGIServer

from .exceptions import *
from .pyhtml import PyHTML
from .defaults import *

def about():
    """
    Returns information about your release and other projects by LK
    """
    return {"Version":(1, 0, 0), "Author":"Leander Kafemann", "date":"07.06.2025",\
            "recommend":("Büro by LK",  "pyimager by LK", "naturalsize by LK"), "feedbackTo": "leander@kafemann.berlin"}

SCHABLONEN = {}
finished = False

def loadFromWeb(url: str, data: dict = {}) -> str:
    """
    Loads content from the given URL with the given data.
    """
    if finished:
        raise ServerAlreadyGeneratedError()
    if not url.endswith(".pyhtml"):
        raise InvalidFiletypeError()
    rq = requests.post(url, data).content
    return rq.decode()

def loadFromFile(filename: str) -> str:
    """
    Loads a file from the given filename.
    """
    if finished:
        raise ServerAlreadyGeneratedError()
    if not filename.endswith(".pyhtml"):
        raise InvalidFiletypeError()
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def addSchablone(name: str, content: str):
    """
    Adds a template to the SCHABLONEN dictionary.
    """
    global SCHABLONEN
    SCHABLONEN += {name: PyHTML(content)}

def makeApplicationObject(contentGeneratingFunction: Callable) -> Callable:
    """
    Returns a WSGI application object based on your contentGeneratingFunction.
    The contentGeneratingFunction should take a single argument (the path) and return the content as a string.
    """
    if not callable(contentGeneratingFunction):
        raise InvalidCallableError()
    def simpleApplication(environ, start_response) -> list:
        """
        A simple WSGI application object that serves as a template.
        """
        type_ = "text/html" 
        status = "200 OK"
        content = contentGeneratingFunction(environ["PATH_INFO"])
        headers = [("Content-Type", type_),
                   ("Content-Length", str(len(content))),
                   ('Access-Control-Allow-Origin', '*')]
        start_response(status, headers)
        return [content.encode("utf-8")]
    return simpleApplication

def setUpServer(application: Callable) -> WSGIServer:
    """
    Creates a WSGI server.
    No additional Schablonen can be loaded from the web.
    """
    global finished
    finished = True
    server = make_server('', 8000, application)
    return server