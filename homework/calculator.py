"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import operator

def home_page():
  page = """
      <h1>In Browser Calculator Instructions</h1>
      <h2>The following operations are supported:</h2>
      <table>
      <tr><th>Add: EX: localhost/add/4/2=6</td></tr>
      <tr><th>Subtract: EX: localhost/subtract/4/2=2</td></tr>
      <tr><th>Multiply: localhost/multiply/4/2=8</td></tr>
      <tr><th>Divide: localhost/divide/4/2=2</td></tr>"""
  return page

def convert_args_to_int(args):
  """Function creates a list of integers given a list of string type integers"""
  int_args = [float(arg) for arg in args]
  start = int_args.pop(0)
  return start, int_args

def operation(math_func, *args):
  """Perform an operation on each item in list"""  
  start, int_args = convert_args_to_int(args)
  for n in int_args:
    start = math_func(start,n)
  return str(start)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    args = path.strip("/").split("/")
    func_name = args.pop(0)
    #dictionary to hold operation functions
    func = {
        'add': operator.iadd,
        'subtract': operator.isub,
        'multiply': operator.imul,
        'divide': operator.itruediv,
    }.get(func_name)
    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        if None in (func, args):
          body = home_page()
        else:
          body = operation(func, *args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        #will raise if user requests a number divided by 0
        status = "500 Internal Server Error"
        body = "<h1> Can't Divide by Zero </h1>"
    except ValueError:
        #will raise if user inputs a non-numeric value
        status = "500 Internal Server Error"
        body = "<h1> Can't Perform Operations on Non Numeric Inputs </h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # DONE: Insert boilerplate wsgiref
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()