import json
from tornado.gen import coroutine
from tornado.web import RequestHandler

class BaseApi(RequestHandler):
    """Base view for this application."""

    def prepare(self):
        self.incoming_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))


class CognitiveApi(BaseApi):
    """View for reading and adding new things."""
    SUPPORTED_METHODS = ("GET", "POST",)

    @coroutine
    def get(self, username):
        self.send_response({
            'username': username,
            'description': "Get call"
        })

    @coroutine
    def post(self, username):
        self.send_response({
            'username': username,
            'description': "Post call"
        })