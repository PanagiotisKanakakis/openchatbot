import os
from configparser import ConfigParser

from flask import Flask, request
from flask_restplus import Resource, Api, fields
from werkzeug import secure_filename, FileStorage
from werkzeug.middleware.proxy_fix import ProxyFix

from core.chatbot import *

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

api = Api(app)

# init configuration variables
config = ConfigParser()
config.read("config/app_config.ini")
host = config.get('general', 'host')
port = config.get('general', 'port')
uploadFolder = config.get('general', 'uploadFolder')

# init chatbot
chatbot = init()

# parameters for swagger api
name_space = api.namespace('chatterbot', description='Chatterbot Core Code API')
question = api.model('question_data', {
    'question': fields.String(description="Question for chatterbot engine", required=True)
})
file = api.parser()
file.add_argument('file', type=FileStorage, location='files', required=True)


@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())


@name_space.route("/applyQuestion")
class chatterBotQuestion(Resource):
    @api.doc(responses={400: "Empty question to chatterbot", 200: "OK"})
    @api.expect(question)
    def post(self):
        return generateResponse(chatbot, request.json['question'])


@name_space.route("/train")
class chatterBotTrain(Resource):
    @api.doc(responses={400: "Empty File", 200: "OK"})
    @api.expect(file, validate=True)
    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(uploadFolder, filename))
            train(uploadFolder + "/" + filename)
            return 'file uploaded successfully'


# @name_space.route("/trainTensorFlow")
# class chatterBotTensorflowTrain(Resource):
#     @api.doc(responses={400: "Empty File", 200: "OK"})
#     @api.expect(file, validate=True)
#     def post(self):
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             return 'No file part'
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             return 'No selected file'
#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(uploadFolder, filename))
#             trainTensorFlowModel(uploadFolder + "/" + filename)
#             return 'file uploaded successfully'
#

if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(debug=True, host=host, port=port)
