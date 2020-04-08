import logging

from chatterbot import ChatBot, comparisons, response_selection
from chatterbot.trainers import ChatterBotCorpusTrainer

logging.basicConfig(level=logging.INFO)


def init():
    chatbot = ChatBot(
        "Charlie",
        read_only=True,
        # storage_adapter='storageAdapter.CustomStorageAdapter',
        logic_adapters=[
            {
                "import_path": "core.logicAdapter.MyLogicAdapter"
            }
        ],
        statement_comparison_function=comparisons.levenshtein_distance,
        response_selection_method=response_selection.get_first_response,
    )
    return chatbot


def train(chatbot, file):
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(file)


def generateResponse(chatbot, question):
    return chatbot.get_response(question).text
