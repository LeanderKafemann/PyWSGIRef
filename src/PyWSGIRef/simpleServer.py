"""
Main method creating simple server example...
"""

from PyWSGIRef import *

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