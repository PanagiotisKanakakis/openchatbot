import requests


class HttpClient:

    def __init__(self, config):
        self.baseUrl = config.get('db-api', 'host')
        self.getAllLanguages()

    def getAllLanguages(self):
        return requests.get(self.baseUrl + "/languages").json()

    def getAllTopics(self):
        return requests.get(self.baseUrl + "/topics").json()

    def getQuestionPerTopicAndLanguage(self, topicId, languageCode):
        return requests.get(self.baseUrl + "/questions/"+languageCode+"/"+str(topicId)).json()
