import json

from chatterbot.conversation import Statement
from chatterbot.trainers import Trainer


class ChatterBotWordSimilarityTrainer(Trainer):

    def train(self, *corpus_paths):
        for file_path in corpus_paths:
            with open(file_path, "r", encoding='utf-8') as json_data:
                intents = json.load(json_data)
                statements_to_create = []

                for QnA in intents['conversations']:
                    for pattern in QnA['patterns']:
                        response = QnA['responses'][0]

                        statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(response)
                        search_in_response_to = self.chatbot.storage.tagger.get_bigram_pair_string(pattern)
                        statement = Statement(
                            text=response,
                            search_text=statement_search_text,
                            in_response_to=pattern,
                            search_in_response_to=search_in_response_to,
                            conversation='training'
                        )
                        statement = self.get_preprocessed_statement(statement)
                        statements_to_create.append(statement)

                        pattern_pair = self.chatbot.storage.tagger.get_bigram_pair_string(pattern)
                        statement = Statement(
                            text=pattern,
                            search_text=pattern_pair,
                            conversation='training'
                        )
                        statement = self.get_preprocessed_statement(statement)
                        statements_to_create.append(statement)

            self.chatbot.storage.create_many(statements_to_create)
