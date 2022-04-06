# __init__.py
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from omniscient.server import LanguageDetectionHandler

define('port', default=3000, help='port to listen on')

def main():
    app = Application([
        ("/text/analytics/languages/", LanguageDetectionHandler)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()