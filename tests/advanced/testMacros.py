from PyWSGIRef import *

# enable beta mode
BETA.enable()

addSchablone("helloWorld", loadFromFile("./shortcutHelloWorld.pyhtml"))

# load macros first
addMacro("helloWorld", PyHTML(loadFromFile("./macroHelloWorld.pyhtml")))
addMacro("time", PyHTML(loadFromFile("./macroTime.pyhtml")))

addSchablone("macroTest", loadFromFile("./macroTest.pyhtml"))

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
        case "/macro":
            return SCHABLONEN["macroTest"].decoded()
            # successfull
        case _:
            return "404 Not Found"

application = makeApplicationObject(contentGeneratingFunction, getStats=True)
server = setUpServer(application)

print("Successfully started WSGI server on port 8000.")
server.serve_forever()