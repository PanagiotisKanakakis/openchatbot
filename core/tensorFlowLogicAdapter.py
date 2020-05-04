# import pickle
#
# from chatterbot.conversation import Statement
# from chatterbot.logic import LogicAdapter
#
# from core.model.tensorFlow.tensorFlowClassifier import TensorFlowClassifier
# from core.model.tensorFlow.tensorFlowTrainer import ChatterBotTensorFlowTrainer
#
#
# class TensorFlowLogicAdapter(LogicAdapter):
#     def __init__(self, chatbot, **kwargs):
#         super().__init__(chatbot, **kwargs)
#         self.excluded_words = []
#
#     def can_process(self, statement):
#         return True
#
#     def process(self, input_statement, additional_response_selection_parameters):
#         data = pickle.load(open("training_data", "rb"))
#         clf = TensorFlowClassifier(ChatterBotTensorFlowTrainer.get_model(data), data)
#         results = clf.classify(input_statement.text)
#         # if we have a classification then find the matching intent tag
#         if results:
#             response = Statement(text=results[0][1])
#             response.confidence = results[0][2]
#             return response
