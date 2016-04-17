import operator

def home_page():
  """"Home page with instructions to use calculator"""
  page = """
      <h1>In Browser Calculator Instructions</h1>
      <h2>The following operations are supported:</h2>
      <table>
      <tr><th>Add: EX: localhost/add/4/2 will return 6</td></tr>
      <tr><th>Subtract: EX: localhost/subtract/4/2 will return 2</td></tr>
      <tr><th>Multiply: EX: localhost/multiply/4/2 will return 8</td></tr>
      <tr><th>Divide: EX: localhost/divide/4/2 will return 2</td></tr>"""
  return page

def operation(math_func, *args):
  """Perform an operation on each item in list"""  
  int_args = [float(arg) for arg in args]
  start = int_args.pop(0)
  for n in int_args:
    start = math_func(start,n)
  return str(start)

def resolve_path(path):
    """Parses request to return a mathemamtical operation and numeric variables"""
    args = path.strip("/").split("/")
    func_name = args.pop(0)
    #dictionary to hold supported operations
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
        #if func and args are blank then no operation was selected - return homepage
        if None in (func, args):
          body = home_page()
        #else pass operaton and args and return result
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
    #Inserted boilerplate wsgiref
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()