import json
from server.language_detection import LanguageDetect
from tornado.escape import json_decode
from tornado.gen import coroutine
from tornado.web import HTTPError, RequestHandler

class BaseApi(RequestHandler):
    """Base view for this application."""

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
    LANGUAGE = LanguageDetect()

    @coroutine
    def get(self, username):
        self.send_response({
            'username': username,
            'description': "Get call"
        })

    @coroutine
    def post(self):
        body = json_decode(self.request.body)
        if 'documents' not in body:
            raise HTTPError(400, "Index name not specified")
        documents = body['documents']
        text = documents[0]['text']
        self.send_response({
            'id': documents[0]['id'],
            'detected_language': self.LANGUAGE.predict_language(text)
        })