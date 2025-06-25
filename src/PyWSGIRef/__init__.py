"""
PYWSGIREF
"""
from typing import Callable
from wsgiref.simple_server import make_server, WSGIServer
from cgi import FieldStorage

from .exceptions import *
from .pyhtml import PyHTML
from .defaults import *
from .templateDict import TemplateDict
from .beta import BETA
from .loadContent import *
from .finished import finished

def about():
    """
    Returns information about your release and other projects by Leander Kafemann
    """
    return {"Version": (1, 1, 11), "Author": "Leander Kafemann", "date": "25.06.2025",\
            "recommend": ("Buero by LK",  "pyimager by LK"), "feedbackTo": "leander@kafemann.berlin"}

SCHABLONEN = TemplateDict()

def addSchablone(name: str, content: str):
    """
    Adds a template to the SCHABLONEN dictionary.
    """
    global SCHABLONEN
    if finished.value:
        raise ServerAlreadyGeneratedError()
    SCHABLONEN[name] = PyHTML(content)

def makeApplicationObject(contentGeneratingFunction: Callable, advanced: bool = False, setAdvancedHeaders: bool = False) -> Callable:
    """
    Returns a WSGI application object based on your contentGeneratingFunction.
    The contentGeneratingFunction should take a single argument (the path) and return the content as a string.
    If advanced is True, the contentGeneratingFunction will receive a FieldStorage object as the second argument.
    If setAdvancedHeaders is True, it will allow you to set advanced headers for the response.
    """
    if not callable(contentGeneratingFunction):
        raise InvalidCallableError()
    def simpleApplication(environ, start_response) -> list:
        """
        A simple WSGI application object that serves as a template.
        """
        type_ = "text/html" 
        status = "200 OK"
        if advanced:
            storage = FieldStorage(fp=environ.get("wsgi.input"), environ=environ, keep_blank_values=True)
            if setAdvancedHeaders:
                content, type_, status = contentGeneratingFunction(environ["PATH_INFO"], storage)
            else:
                content = contentGeneratingFunction(environ["PATH_INFO"], storage)
        else:
            if setAdvancedHeaders:
                raise AdvancedHeadersWithoutAdvancedModeError()
            content = contentGeneratingFunction(environ["PATH_INFO"])
        headers = [("Content-Type", type_),
                   ("Content-Length", str(len(content))),
                   ('Access-Control-Allow-Origin', '*')]
        start_response(status, headers)
        return [content.encode("utf-8")]
    return simpleApplication

def setUpServer(application: Callable, port: int = 8000) -> WSGIServer:
    """
    Creates a WSGI server.
    No additional Schablonen can be loaded from the web.
    """
    finished.set_true()
    server = make_server('', port, application)
    return server