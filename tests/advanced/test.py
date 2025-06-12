from PyWSGIRef import *

# enable beta mode
BETA.enable()

addSchablone("helloWorld", loadFromFile("./shortcutHelloWorld.pyhtml"))
addSchablone("includeStyleTest", loadFromFile("./includeStyleTest.pyhtml"))
addSchablone("scriptInclusionTest", loadFromFile("./scriptInclusionTest.pyhtml"))

def contentGeneratingFunction(path: str) -> str:
    """
    A simple content generating function that returns a greeting.
    """
    match path:
        case "/":
            return MAIN_HTML.format(about()["Version"])
        case "/hello":
            return SCHABLONEN["helloWorld"].decoded()
        case "/includeStyleTest":
            return SCHABLONEN["includeStyleTest"].decoded()
        case "/scriptInclusionTest":
            return SCHABLONEN["scriptInclusionTest"].decoded()
        case _:
            return "404 Not Found"

application = makeApplicationObject(contentGeneratingFunction)
server = setUpServer(application)

print("Successfully started WSGI server on port 8000.")
server.serve_forever()