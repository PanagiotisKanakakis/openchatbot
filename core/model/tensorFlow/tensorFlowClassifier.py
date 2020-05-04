# import nltk
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from nltk.stem.lancaster import LancasterStemmer
#
#
# class TensorFlowClassifier:
#
#     def __init__(self, model, data):
#         self.model = model
#         self.data = data
#
#     def clean_up_sentence(self, sentence):
#         stemmer = LancasterStemmer()
#         # tokenize the pattern
#         sentence_words = nltk.word_tokenize(sentence)
#         # stem each word
#         sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
#         return sentence_words
#
#     # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
#     def bow(self, sentence, show_details=False):
#         # tokenize the pattern
#         sentence_words = self.clean_up_sentence(sentence)
#         # bag of words
#         bag = [0] * len(self.data['words'])
#         for s in sentence_words:
#             for i, w in enumerate(self.data['words']):
#                 if w == s:
#                     bag[i] = 1
#                     if show_details:
#                         print("found in bag: %s" % w)
#
#         return np.array(bag)
#
#     def classify(self, sentence):
#         classes = self.data['classes']
#         responses = self.data['responses']
#         predict_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
#             {'sentence': pd.DataFrame([sentence]).values}, shuffle=False)
#         predictions = self.model.predict(input_fn=predict_input_fn)
#         for pred_dict in predictions:
#             class_id = pred_dict['class_ids'][0]
#             probability = pred_dict['probabilities'][class_id]
#             return_list = [(classes[class_id], responses[class_id], probability)]
#         return return_list
#         # ERROR_THRESHOLD = 0.25
#         # words = self.data['words']
#         # classes = self.data['classes']
#         # responses = self.data['responses']
#         # # generate probabilities from the model
#         # results = self.model.predict([self.bow(sentence, words)])[0]
#         # # filter out predictions below a threshold
#         # results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
#         # # sort by strength of probability
#         # results.sort(key=lambda x: x[1], reverse=True)
#         # return_list = []
#         # for r in results:
#         #     return_list.append((classes[r[0]], responses[r[0]], r[1]))
#         # # return tuple of intent and probability
#         # return return_list
