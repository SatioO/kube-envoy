import os
import socket
import sys

import requests
from flask import Flask, request

app = Flask(__name__)

TRACE_HEADERS_TO_PROPAGATE = [
    'X-Ot-Span-Context',
    'X-Request-Id',

    # Zipkin headers
    'X-B3-TraceId',
    'X-B3-SpanId',
    'X-B3-ParentSpanId',
    'X-B3-Sampled',
    'X-B3-Flags',

    # Jaeger header (for native client)
    "uber-trace-id",

    # Custom Headers
    "Session-Id",
    "Correlation-Id"
]


@app.route('/')
def hello_geek():
    return '<h1>Hello from {}</h2>'.format(os.environ['SERVICE_NAME'])

@app.route('/service/<service_number>')
def hello(service_number):
  return ('Hello from behind Envoy (service {})! hostname: {} resolved'
          'hostname: {}\n'.format(os.environ['SERVICE_NAME'], socket.gethostname(),
                                  socket.gethostbyname(socket.gethostname())))


@app.route('/trace/<service_number>')
def trace(service_number):
  headers = {}
  # call service 2 from service 1
  if int(os.environ['SERVICE_NAME']) == 1:
    for header in TRACE_HEADERS_TO_PROPAGATE:
      if header in request.headers:
        headers[header] = request.headers[header]
    requests.get("http://service2:8000/trace/2", headers=headers)
  return ('Hello from behind Envoy (service {})! hostname: {} resolved'
          'hostname: {}\n'.format(os.environ['SERVICE_NAME'], socket.gethostname(),
                                  socket.gethostbyname(socket.gethostname())))


if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5000, debug=True)
