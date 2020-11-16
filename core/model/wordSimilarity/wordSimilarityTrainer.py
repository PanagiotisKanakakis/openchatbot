from chatterbot.conversation import Statement
from chatterbot.trainers import Trainer


class ChatterBotWordSimilarityTrainer(Trainer):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.httpClient = None

    def setHttpClient(self, httpClient):
        self.httpClient = httpClient

    def train(self, *corpus_paths):
        languages = self.httpClient.getAllLanguages()

        for language in languages:
            statements_to_create = []
            languageCode = language['code']
            questions = self.httpClient.getQuestionsPerLanguage(languageCode)
            for question in questions:
                answer = question['answer']
                response = answer['description']
                question = question['description']
                statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(response)
                search_in_response_to = self.chatbot.storage.tagger.get_bigram_pair_string(question)
                statement = Statement(
                    text=response,
                    search_text=statement_search_text,
                    in_response_to=question,
                    search_in_response_to=search_in_response_to,
                    conversation='training'
                )
                statement = self.get_preprocessed_statement(statement)
                statements_to_create.append(statement)

                pattern_pair = self.chatbot.storage.tagger.get_bigram_pair_string(question)
                statement = Statement(
                    text=question,
                    search_text=pattern_pair,
                    conversation='training'
                )
                statement = self.get_preprocessed_statement(statement)
                statements_to_create.append(statement)
            self.chatbot.storage.create_many(statements_to_create)
