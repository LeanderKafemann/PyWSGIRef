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
from .stats import Stats

def about():
    """
    Returns information about your release and other projects by Leander Kafemann
    """
    return {"Version": (1, 1, 16), "Author": "Leander Kafemann", "date": "05.09.2025",\
            "recommend": ("pyimager"), "feedbackTo": "leander.kafemann+python@icloud.com"}

SCHABLONEN = TemplateDict()
STATS = Stats()

def addSchablone(name: str, content: str):
    """
    Adds a template to the SCHABLONEN dictionary.
    """
    global SCHABLONEN
    if finished.value:
        raise ServerAlreadyGeneratedError()
    SCHABLONEN[name] = PyHTML(content)

def makeApplicationObject(contentGeneratingFunction: Callable, advanced: bool = False, setAdvancedHeaders: bool = False,\
                          getIP: bool = False, vercelPythonHosting: bool = False, getStats: bool = False) -> Callable:
    """
    Returns a WSGI application object based on your contentGeneratingFunction.
    The contentGeneratingFunction should take a single argument (the path) and return the content as a string.
    If advanced is True, the contentGeneratingFunction will receive a FieldStorage object as the second argument.
    If setAdvancedHeaders is True, it will allow you to set advanced headers for the response.
    If getIP is True, the contentGeneratingFunction will receive the IP address of the client as an additional argument.
    If vercelPythonHosting is True, your application object will be optimized for Vercel's unusual WSGI methods.
    If getStats is True, stats are saved in the STATS object (BETA).
    Locks BETA mode.
    """
    if not callable(contentGeneratingFunction):
        raise InvalidCallableError()
    BETA.lock()
    def simpleApplication(environ, start_response) -> list:
        """
        A simple WSGI application object that serves as a template.
        """
        if getStats:
            if not BETA.value:
                raise BetaNotEnabledError()
            STATS.count.increase()
            perfTime = STATS.startPerfTime("applicationCallNr"+str(STATS.count.count))
        type_ = "text/html" 
        status = "200 OK"
        if advanced:
            storage = FieldStorage(fp=environ.get("wsgi.input"), environ=environ, keep_blank_values=True)
            if setAdvancedHeaders:
                if getIP:
                    content, type_, status = contentGeneratingFunction(environ["PATH_INFO"], storage, environ["HTTP_X_REAL_IP"])
                else:
                    content, type_, status = contentGeneratingFunction(environ["PATH_INFO"], storage)
            else:
                if getIP:
                    content = contentGeneratingFunction(environ["PATH_INFO"], storage, environ["HTTP_X_REAL_IP"])
                else:
                    content = contentGeneratingFunction(environ["PATH_INFO"], storage)
        else:
            if setAdvancedHeaders:
                raise AdvancedHeadersWithoutAdvancedModeError()
            if getIP:
                content = contentGeneratingFunction(environ["PATH_INFO"], environ["HTTP_X_REAL_IP"])
            else:
                content = contentGeneratingFunction(environ["PATH_INFO"])
        headers = [("Content-Type", type_),
                   ("Content-Length", str(len(content))),
                   ('Access-Control-Allow-Origin', '*')]
        start_response(status, headers)
        if getStats:
            STATS.stopPerfTime(perfTime)
        if not vercelPythonHosting:
            return [content.encode("utf-8")]
    return simpleApplication

def setUpServer(application: Callable, port: int = 8000) -> WSGIServer:
    """
    Creates a WSGI server.
    No additional templates can be loaded from the web.
    """
    finished.set_true()
    server = make_server('', port, application)
    return server