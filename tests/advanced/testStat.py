from PyWSGIRef import *

#test successfull

# enable beta mode
BETA.enable()

addSchablone("helloWorld", loadFromFile("./shortcutHelloWorld.pyhtml"))
addSchablone("evalTest", loadFromFile("./evalTest.pyhtml"))

def contentGeneratingFunction(path: str) -> str:
    """
    A simple content generating function that returns a greeting.
    """
    match path:
        case "/":
            return MAIN_HTML.format(about()["Version"])
            # successfull
        case "/hello":
            return SCHABLONEN["helloWorld"].decoded()
            # successfull
        case "/evalTest":
            import datetime
            return SCHABLONEN["evalTest"].decodedContext(locals())
            # successful
        case "/stats":
            return STATS.export_stats()
        case _:
            return "404 Not Found"

application = makeApplicationObject(contentGeneratingFunction, getStats=True)
server = setUpServer(application)

print("Successfully started WSGI server on port 8000.")
server.serve_forever()