# PyWSGIRef
easy server-setup
## Advantage
Many web services offer simple ways to set up a WSGI webserver.<br/>
The built-in WSGI server in Python is, however, not very easy to use.<br/>
PyWSGIRef provides a simple way to set up a WSGI server with minimal code.<br/><br/>
Also, a problem with many of those web services is that they aren't able to make web requests<br/>
and it's very slow to read files once the server is running.<br/>
PyWSGIRef solves this problem by providing a simple way to load PyHTML files from the web or from the local filesystem<br/>
before the server is running.<br/><br/>
PyHTML files are HTML files that can contain {}-s for Python formatting or<br/>
(upcoming) code blocks or shortened HTML, which can be used to create dynamic HTML content.<br/>
PyWSGIRef also provides a simple way to decode these.
## Installation
### Using *pip*
You can install PyWSGIRef via pip using
<li>in a commandline:</li><br/>

```bash
py -m pip install PyWSGIRef
```
<br/>
<li>in a python script:</li><br/>

```python
import os
os.system('py -m pip install PyWSGIRef')
```
## Usage
### Setting up the WSGI server
```python
from PyWSGIRef import *

# Create a WSGI application object
def simple_app(path: str) -> str:
	return f"Hello, you visited {path}!"
application = makeWSGIApp(simple_app)

# Create a WSGI server
server = makeWSGIServer(application, port=8000)
server.serve_forever()
```
The <code>makeWSGIApp</code> function requires a callable that takes a single argument (the path) and returns a string response.<br/>
The <code>makeWSGIServer</code> function creates a WSGI server that listens on the specified port (default is 8000)<br/>
and calls the application object with the environ.<br/>
You can also use your own application object instead of the one created by <code>makeWSGIApp</code>.
### Loading PyHTML
PyWSGIRef also provides a simple way to load PyHTML files:
```python
from PyWSGIRef import *

# load from file
html = loadFromFile('index.pyhtml')

# load from web
html = loadFromWeb('https://example.com/index.pyhtml')
```
This is useful for serving dynamic HTML content in your WSGI application.<br/>
The funcs are callable unless you set up a server.
### Using Templates
PyWSGIRef also provides a simple way to use templates in your WSGI application:
```python
from PyWSGIRef import *

# add template to template dictionary
# -> saves as PyHTML object
addSchablone("index", loadedPyHTMLFile)

# load template from dictionary
# get HTML code from PyHTML object
html = SCHABLONEN["index"].decoded()
# use Python formatting
serverPageContent = html.format("Hello, World!")
```
Note that you may only use the <code>addSchablone</code> function before you set up a server.
### Default HTML templates
PyWSGIRef comes with some default HTML templates that you can use in your WSGI application.<br/>
You can access them via the <code>PyWSGIRef.defaults</code>:
```python
from PyWSGIRef import *

# load default HTML template
addSchablone("hello", HELLO_WORLD)
addSchablone("error", ERROR)
```
### __main__ script
You may produce a simple WSGI server by using either:<br/>
```python
from PyWSGIRef import *

main()
```
or (from a commandline)
```bash
py -m PyWSGIRef
```
### Others
Use the following to get information about your release and the author of the module:
```python
pycols.about()
```
### More coming soon