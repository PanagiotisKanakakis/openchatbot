import logging

from chatterbot import ChatBot, comparisons, response_selection
from chatterbot.trainers import ChatterBotCorpusTrainer

from core.model.fastText.fastTextTrainer import ChatterBotFastTextTrainer
from core.model.tensorFlow.tensorFlowTrainer import ChatterBotTensorFlowTrainer

logging.basicConfig(level=logging.INFO)

tensorFlowTrainer = None
trainer = None


def init():
    chatbot = ChatBot(
        "Charlie",
        read_only=True,
        # storage_adapter='storageAdapter.CustomStorageAdapter',
        logic_adapters=[
            {
                "import_path": "core.tensorFlowLogicAdapter.TensorFlowLogicAdapter"
            },
            {
                "import_path": "core.logicAdapter.MyLogicAdapter"
            },
            {
                "import_path": "core.fastTextLogicAdapter.FastTextLogicAdapter"
            }


        ],
        statement_comparison_function=comparisons.levenshtein_distance,
        response_selection_method=response_selection.get_first_response,
    )
    global trainer, tensorFlowTrainer, fastTextTrainer
    tensorFlowTrainer = ChatterBotTensorFlowTrainer(chatbot)
    fastTextTrainer = ChatterBotFastTextTrainer(chatbot)
    trainer = ChatterBotCorpusTrainer(chatbot)
    return chatbot


def train(file):
    trainer.train(file)
    tensorFlowTrainer.train(file)
    fastTextTrainer.train(file)


def generateResponse(chatbot, question):
    return chatbot.get_response(question).text


def trainTensorFlowModel(file):
    return tensorFlowTrainer.train(file)
