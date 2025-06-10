HELLO_WORLD = """<!DOCTYPE html>
<html lang"de">
    <body>
        <h1>Hallo Welt!</h1>
    </body>
<html>"""

ERROR = """<!DOCTYPE html>
<html lang"de">
    <body>
        <h1>Fehler!</h1>
        <p>Es ist ein Fehler aufgetreten.</p>
    </body>
</html>"""

MAIN_HTML = """<!DOCTYPE html>
<html lang="de">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>PyWSGIRef Server</title>
    </head>
    <body>
        <h1>Willkommen zum PyWSGIRef Server!</h1>
        <p>Dies ist die Hauptseite des Servers.</p>
        <p>Sie nutzen Version {} von PyWSGIRef.</p>
    </body>
</html>"""

SHUTDOWN_HTML = """<!DOCTYPE html>
<html lang="de">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Server Shutdown</title>
    <body>
        <h1>Server Shutdown</h1>
        <p>
            Der Server wird jetzt heruntergefahren.
        </p>
    </body>
</html>"""