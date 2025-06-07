"""
Set up and run the PyWSGIRef server with a simple HTML response.
"""
from PyWSGIRef import *

def main():
    """
    Main function to set up and run the PyWSGIRef server.
    """
    # define main html response
    MAIN_HTML = """<!DOCTYPE html>
    <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PyWSGIRef Server</title>
        </head>
        <body>
            <h1>Willkommen zum PyWSGIRef Server!</h1>
            <p>Dies ist die Hauptseite des Servers.</p>
            <p>Sie nutzen Version {} von PyWSGIRef.</p>
        </body>
    </html>"""

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

if __name__ == "__main__":
    main()