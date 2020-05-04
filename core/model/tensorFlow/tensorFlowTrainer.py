# import json
# import pickle
# import time
# from functools import partial
#
# import pandas as pd
# import tensorflow as tf
# import tensorflow_hub as hub
# from chatterbot.trainers import Trainer
# from nltk.stem.lancaster import LancasterStemmer
#
#
# class ChatterBotTensorFlowTrainer(Trainer):
#     """
#     Allows the chat bot to be trained using data from the
#     ChatterBot dialog corpus.
#     """
#
#     model = None
#
#     def train(self, *corpus_paths):
#
#         for file_path in corpus_paths:
#             words, classes, documents, responses = self.getTrainingData(file_path)
#             train_questions, train_labels = self.transformDataToModelFormat(words, classes, documents)
#             self.trainModel(train_questions, train_labels)
#             pickle.dump(
#                 {'words': words, 'classes': classes, 'responses': responses, 'train_questions': train_questions,
#                  'train_labels': train_labels},
#                 open("training_data", "wb"))
#
#     def getTrainingData(self, *corpus_path):
#         stemmer = LancasterStemmer()
#         counter = 0
#         with open(*corpus_path) as json_data:
#             intents = json.load(json_data)
#             words = []
#             classes = []
#             responses = []
#             documents = []
#             ignore_words = ['?']
#             # loop through each sentence in our intents patterns
#             for QnA in intents['conversations']:
#                 question = QnA[0]
#                 answer = QnA[1]
#                 # add to documents in our corpus
#                 documents.append(question)
#                 responses.append(answer)
#                 # add to our classes list
#                 if '__label__QnA' + str(counter) not in classes:
#                     print('__label__QnA' + str(counter), question)
#                     classes.append(counter)
#                 counter += 1
#             # for QnA in intents['conversations']:
#             #     question = QnA[0]
#             #     answer = QnA[1]
#             #     # tokenize each word in the sentence
#             #     w = nltk.word_tokenize(question)
#             #     # add to our words list
#             #     words.extend(w)
#             #     # add to documents in our corpus
#             #     documents.append((w, '__label__QnA' + str(counter)))
#             #     responses.append(answer)
#             #     # add to our classes list
#             #     if '__label__QnA' + str(counter) not in classes:
#             #         print('__label__QnA' + str(counter), question)
#             #         classes.append('__label__QnA' + str(counter))
#             #     counter += 1
#
#             # stem and lower each word and remove duplicates
#             words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
#             words = sorted(list(set(words)))
#             # remove duplicates
#             classes = sorted(list(set(classes)))
#             return words, classes, documents, responses
#
#     def transformDataToModelFormat(self, words, classes, documents):
#         docs = pd.DataFrame(documents)
#         cls = pd.DataFrame(classes)
#
#         return docs.values, cls.values
#
#         # # create our training data
#         # training = []
#         # output = []
#         # # create an empty array for our output
#         # output_empty = [0] * len(classes)
#         # stemmer = LancasterStemmer()
#         #
#         # # training set, bag of words for each sentence
#         # for doc in documents:
#         #     # initialize our bag of words
#         #     bag = []
#         #     # list of tokenized words for the pattern
#         #     pattern_words = doc[0]
#         #     # stem each word
#         #     pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
#         #     # create our bag of words array
#         #     for w in words:
#         #         bag.append(1) if w in pattern_words else bag.append(0)
#         #
#         #     # output is a '0' for each tag and '1' for current tag
#         #     output_row = list(output_empty)
#         #     output_row[classes.index(doc[1])] = 1
#         #
#         #     training.append([bag, output_row])
#         #
#         # # shuffle our features and turn into np.array
#         # random.shuffle(training)
#         # training = np.array(training)
#         #
#         # # create train and test lists
#         # train_x = list(training[:, 0])
#         # train_y = list(training[:, 1])
#         # return train_x, train_y
#
#     @classmethod
#     def trainModel(cls, train_questions, train_labels):
#         train_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
#             {'sentence': train_questions}, train_labels,
#             batch_size=256, num_epochs=None, shuffle=True)
#
#         # Prediction on the whole training set.
#         predict_train_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
#             {'sentence': train_questions}, train_labels, shuffle=False)
#         embedding_feature = hub.text_embedding_column(
#             key='sentence',
#             module_spec="https://tfhub.dev/google/universal-sentence-encoder/2",
#             trainable=False)
#         global model
#         cls.model = tf.estimator.DNNClassifier(
#             hidden_units=[512, 128],
#             feature_columns=[embedding_feature],
#             n_classes=len(train_labels),
#             activation_fn=tf.nn.relu,
#             dropout=0.1,
#             optimizer=tf.optimizers.Adagrad(learning_rate=0.005),
#             model_dir='./model.tflearn')
#
#         TOTAL_STEPS = 1500
#         STEP_SIZE = 100
#         # for step in range(0, TOTAL_STEPS + 1, STEP_SIZE):
#         # print()
#         # print('-' * 100)
#         # print('Training for step =', step)
#         start_time = time.time()
#         cls.model.train(input_fn=train_input_fn, steps=STEP_SIZE)
#         elapsed_time = time.time() - start_time
#         print('Train Time (s):', elapsed_time)
#         print('Eval Metrics (Train):', cls.model.evaluate(input_fn=predict_train_input_fn))
#         # # reset underlying graph data
#         # tf.reset_default_graph()
#         # # Build neural network
#         # net = tflearn.input_data(shape=[None, len(train_x[0])])
#         # net = tflearn.fully_connected(net, 8)
#         # net = tflearn.fully_connected(net, 8)
#         # net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
#         # net = tflearn.regression(net)
#         #
#         # # Define model and setup tensorboard
#         # # global model
#         # cls.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
#         # # Start training (apply gradient descent algorithm)
#         # cls.model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=False)
#         # cls.model.save('model.tflearn')
#
#     @classmethod
#     def get_model(cls, data):
#         if cls.model is None:
#             embedding_feature = hub.text_embedding_column(
#                 key='sentence',
#                 module_spec="https://tfhub.dev/google/universal-sentence-encoder/2",
#                 trainable=False)
#             cls.model = tf.estimator.DNNClassifier(
#                 hidden_units=[512, 128],
#                 feature_columns=[embedding_feature],
#                 n_classes=len(data['train_labels']),
#                 activation_fn=tf.nn.relu,
#                 dropout=0.1,
#                 optimizer=tf.optimizers.Adagrad(learning_rate=0.005),
#                 model_dir='./model.tflearn')
#             # # reset underlying graph data
#             # tf.reset_default_graph()
#             # # Build neural network
#             # net = tflearn.input_data(shape=[None, len(data['train_x'][0])])
#             # net = tflearn.fully_connected(net, 8)
#             # net = tflearn.fully_connected(net, 8)
#             # net = tflearn.fully_connected(net, len(data['train_y'][0]), activation='softmax')
#             # net = tflearn.regression(net)
#             #
#             # # Define model and setup tensorboard
#             # cls.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
#             # cls.model.load('./model.tflearn')
#         return cls.model
