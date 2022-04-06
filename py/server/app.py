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
    SUPPORTED_METHODS = ("POST")
    LANGUAGE = LanguageDetect()

    @coroutine
    def post(self):
        body = json_decode(self.request.body)
        if 'documents' not in body:
            raise HTTPError(400, "documents not specified")
        documents = body['documents']
        if not (isinstance(documents, list) and len(documents) > 0):
            raise HTTPError(400, "documents must be a non empty array")
        
        output_documents = []
        for input in documents:
            id = input['id']
            text = input['text']
            detected_languages = self.LANGUAGE.predict_language(text)
            output_documents.append({
                "id": id,
                "detectedLanguages": detected_languages
            })
        
        self.send_response({
            "documents": output_documents
        })