from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

from core.model.fastText.fastTextClassifier import FastTextClassifier


class FastTextLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.excluded_words = []
        self.clf = FastTextClassifier('en')
        self.languageCode = 'en'

    def can_process(self, statement):
        return True

    def process(self, input_statement, additional_response_selection_parameters):

        if self.languageCode != additional_response_selection_parameters.get('languageCode'):
            self.clf = FastTextClassifier(additional_response_selection_parameters.get('languageCode'))
            self.languageCode = additional_response_selection_parameters.get('languageCode')

        if additional_response_selection_parameters.get('languageCode') != 'en':
            results = [('', 0.0)]
        else:
            results = self.clf.classify(input_statement.text)
        # if we have a classification then find the matching intent tag
        if results:
            response = Statement(text=results[0][0])
            response.confidence = results[0][1]
            return response
