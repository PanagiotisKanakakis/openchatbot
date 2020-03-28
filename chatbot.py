import logging

from chatterbot import ChatBot, comparisons, response_selection
from chatterbot.trainers import ChatterBotCorpusTrainer

logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    "Charlie",
    logic_adapters=[
        {
            "import_path": "logicAdapter.MyLogicAdapter"
        }
    ],
    # statement_comparison_function=comparisons.jaccard_similarity,
    statement_comparison_function=comparisons.synset_distance,
    response_selection_method=response_selection.get_first_response,
    # maximum_similarity_threshold=0.9
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("/home/panagiotis/ellak/questions.json")

# Get a response to the input text 'I would like to book a flight.'
# response = chatbot.get_response('I would like to book a flight Amsterdam.')
# response = chatbot.get_response('How do I register for selfie')
# print(response)
print(80 * "-")
response = chatbot.get_response('Is there a way to register for selfie?')
print(response)
print(80 * "-")
