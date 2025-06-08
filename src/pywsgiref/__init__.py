"""
PYWSGIREF
"""
from typing import Callable
import requests
from wsgiref.simple_server import make_server, WSGIServer
from cgi import FieldStorage

from .exceptions import *
from .pyhtml import PyHTML
from .defaults import *
from .templateDict import TemplateDict, OneWayBoolean

def about():
    """
    Returns information about your release and other projects by LK
    """
    return {"Version":(1, 1, 0), "Author":"Leander Kafemann", "date":"08.06.2025",\
            "recommend":("Büro by LK",  "pyimager by LK"), "feedbackTo": "leander@kafemann.berlin"}

SCHABLONEN = TemplateDict()
finished = OneWayBoolean()

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
    server = make_server('', 8000, application)
    return server

def main():
    """
    Main function to set up and run the PyWSGIRef server.
    """
    # add Schablone 'Hallo Welt' as main
    addSchablone("main", MAIN_HTML)

    # set up application object
    def contentGenerator(path: str) -> str:
        """
        Serves as the main WSGI application.
        """
        match path:
            case "/":
                content = SCHABLONEN["main"].decoded().format(about()["Version"])
            case "/hello":
                content = HELLO_WORLD
            case _:
                content = ERROR
        return content

    # make the application object
    application = makeApplicationObject(contentGenerator)

    # set up server
    server = setUpServer(application)

    # Note: This code is intended to be run as a script, not as a module.
    print("Successfully started WSGI server on port 8000.")

    # start serving
    server.serve_forever()