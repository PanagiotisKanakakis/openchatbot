import logging

from chatterbot import ChatBot, comparisons, response_selection

from core.model.fastText.fastTextTrainer import ChatterBotFastTextTrainer
from core.model.wordSimilarity.wordSimilarityTrainer import ChatterBotWordSimilarityTrainer

logging.basicConfig(level=logging.INFO)

tensorFlowTrainer = None
trainer = None


def initLevenshtein():
    global trainer
    chatbot = ChatBot(
        "Charlie",
        read_only=True,
        database_uri='sqlite:///database.db',
        logic_adapters=[
            {
                "import_path": "core.logicAdapter.MyLogicAdapter"
            }
        ],
        statement_comparison_function=comparisons.levenshtein_distance,
        response_selection_method=response_selection.get_first_response,
    )
    trainer = ChatterBotWordSimilarityTrainer(chatbot)
    return chatbot


def initFastText():
    global fastTextTrainer
    chatbot = ChatBot(
        "FastText",
        read_only=True,
        # storage_adapter='core.storageAdapter.CustomStorageAdapter',
        logic_adapters=[
            {
                "import_path": "core.fastTextLogicAdapter.FastTextLogicAdapter"
            }
        ]
    )
    fastTextTrainer = ChatterBotFastTextTrainer(chatbot)
    return chatbot


def train(file):
    fastTextTrainer.train(file)
    trainer.train(file)


def generateResponse(chatbotLevenshtein, chatbotFastText, question):
    s1 = chatbotLevenshtein.get_response(question)
    s2 = chatbotFastText.get_response(question)
    return [("Levenshtein similarity", s1.text, s1.confidence), ("FastText similarity", s2.text, s2.confidence)]


def trainTensorFlowModel(file):
    return tensorFlowTrainer.train(file)
