#!/usr/bin/env python
import datetime
import os
import sys

default = "No Value Set"

body = """<html>
<head>
<title>Lab 3 - WSGI experiments</title>
</head>
<body>
<p>Hey there, this page has been generated by {software}, running at {path}</p>
<p>Today is {month} {date}, {year}.</p>
<p>This page was requested by IP Address {client_ip}</p>
</body>
</html>"""

date = datetime.date.today()

def application(environ, start_response):
    import pprint
    pprint.pprint(environ)

    response_body = body.format(
        software=environ.get('SERVER_SOFTWARE', default),
        path=os.path.dirname(os.path.realpath(sys.argv[0])),
        month=date.month,
        date=date,
        year=date.year,
        client_ip="eeee"
    )
    status = '200 OK'

    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
