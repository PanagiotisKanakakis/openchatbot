from configparser import ConfigParser

from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Resource, Api, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from core.chatbot import *
from core.http.HttpClient import HttpClient
from core.mailer.MailClient import MailClient

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

# init configuration variables
config = ConfigParser()
config.read("config/app_config.ini")
host = config.get('general', 'host')
port = config.get('general', 'port')
threshold = config.get('general', 'confidence_value_threshold')
httpClient = HttpClient(config)
mailClient = MailClient(config)

# init chatbot
chatbotLevenshtein = initLevenshtein()
chatbotFastText = initFastText(httpClient)

# parameters for swagger api
name_space = api.namespace('chatterbot', description='Chatterbot Core Code API')
question = api.model('question_data', {
    'text': fields.String(description="Question for chatterbot engine", required=True),
    'languageCode': fields.String(description="Language code from a predefined set of codes", required=True)
})
language = api.model('language_data', {
    'language': fields.String(description="Language for frequently asked questions", required=True)
})


@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response


@name_space.route("/applyQuestion")
class chatterBotQuestion(Resource):
    @api.doc(responses={400: "Empty question to chatterbot", 200: "OK"})
    @api.expect(question)
    def post(self):
        return generateResponse(mailClient, chatbotLevenshtein, chatbotFastText, request.json['text'],
                                request.json['languageCode'], threshold)


@name_space.route("/frequentlyAskedQuestions")
class frequentlyAskedQuestions(Resource):
    @api.doc(responses={400: "Empty question set", 200: "OK"})
    @api.expect(language)
    def get(self):
        pass
        # return dbHandler.getFrequentlyAskedQuestionsPerLanguage(request.json['language'])


if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(debug=True, host=host, port=port)
