from PyWSGIRef import *

# enable beta mode
BETA.enable()

addSchablone("helloWorld", loadFromFile("./shortcutHelloWorld.pyhtml"))
addSchablone("includeStyleTest", loadFromFile("./includeStyleTest.pyhtml"))
addSchablone("scriptInclusionTest", loadFromFile("./scriptInclusionTest.pyhtml"))
addSchablone("styleInclusionTest", loadFromFile("./styleInclusionTest.pyhtml"))
addSchablone("inclusionTest", loadFromFile("./staticResourceInclusionTest.pyhtml"))
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
        case "/includeStyleTest":
            return SCHABLONEN["includeStyleTest"].decoded()
            # successfull
        case "/scriptInclusionTest":
            return SCHABLONEN["scriptInclusionTest"].decoded()
            # successfull
        case "/styleInclusionTest":
            return SCHABLONEN["styleInclusionTest"].decoded()
            # successfull
        case "/inclusionTest": 
            return SCHABLONEN["inclusionTest"].decoded()
            # successfull
        case "/evalTest":
            import datetime
            return SCHABLONEN["evalTest"].decodedContext(globals())
            # not possible until 1.1.10 or greater
        case _:
            return "404 Not Found"

application = makeApplicationObject(contentGeneratingFunction)
server = setUpServer(application)

print("Successfully started WSGI server on port 8000.")
server.serve_forever()