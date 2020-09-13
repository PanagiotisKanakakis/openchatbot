# import hashlib
#
# import mysql.connector
# from mysql.connector import Error
#
#
# class MySQLDBHandler:
#
#     def __init__(self, config):
#         host = config.get('database', 'host')
#         port = config.get('database', 'port')
#         database = config.get('database', 'database')
#         user = config.get('database', 'user')
#         password = config.get('database', 'password')
#
#         try:
#             self.connection = mysql.connector.connect(user=user,
#                                                       password=password,
#                                                       host=host,
#                                                       port=port,
#                                                       database=database)
#             if self.connection.is_connected():
#                 db_Info = self.connection.get_server_info()
#                 print("Connected to MySQL Server version ", db_Info)
#                 cursor = self.connection.cursor(dictionary=True)
#                 cursor.execute("select database();")
#                 record = cursor.fetchone()
#                 print("You're connected to database: ", record)
#
#         except Error as e:
#             print("Error while connecting to MySQL", e)
#
#     def getAllLanguages(self):
#         sql = """select * from  LANGUAGE l """
#         languages = self.execute_select(sql)
#         return languages
#
#     def getFrequentlyAskedQuestionsPerLanguage(self, question, language):
#         sql = """select *
#                 from QUESTION q, QUESTION_LANGUAGE ql, LANGUAGE l
#                 where q.Id = ql.QuestionId and ql.LanguageId = l.Id and q.Status = 'Published'
#                 and l.Name = '' = '%s'""" % language
#         questions = self.execute_select(sql)
#         return questions
#
#     def getQuestionPerTopicAndLanguage(self, topicId, language):
#         sql = """select *
#                         from QUESTION q, QUESTION_LANGUAGE ql, LANGUAGE l
#                         where q.Id = ql.QuestionId and q.TopicId = '' and ql.LanguageId = l.Id and q.Status = 'Published'
#                         and l.Name = '' = '%s' '%s' """ % topicId % language
#         questions = self.execute_select(sql)
#         return questions
#
#     def getAnswerPerIdAndLanguage(self, id, language):
#         sql = """select *
#                         from ANSWER a, ANSWER_LANGUAGE al, LANGUAGE l
#                         where a.Id = '' and al.LanguageId = l.Id and a.Status = 'Published'
#                         and l.Name = '' = '%s' '%s'""" % id % language
#         answers = self.execute_select(sql)
#         return answers
#
#     def execute_select(self, sql):
#         """
#         Function that execute sql SELECT statement
#         :param self: A class reference with all required options and functions
#         :param sql: The sql SELECT statement
#         :return: A String of topics or 'No Topics' if domain has no topics otherwise an empty string ''
#         """
#         c = self.connection.cursor()
#         c.execute(sql)
#         try:
#             return c.fetchall()
#         except Exception as e:
#             return ''
#
#     def execute_insert(self, sql, values):
#         self.connection.cursor().execute(sql, values)
#         self.connection.commit()
#
#     def storeUser(self, userID):
#         pass
#
#     def storeExperiment(self, userID):
#         pass
#
#     def storePage(self, url, typo):
#         md5 = hashlib.md5(url.encode('utf-8'))
#         sql = """insert ignore into page(type,url,hashed_url) value (%s,%s, %s)"""
#         values = (typo, url, md5.hexdigest())
#         self.execute_insert(sql, values)
#
#     def storeTopics(self, url, topics):
#         for topic in topics:
#             for t in topic:
#                 sql = """insert ignore into topic(name) value (%s)"""
#                 self.execute_insert(sql, (t,))
#                 sql = """insert ignore into page_has_topic(pageId,topicId)
#                          value (
#                                 (select id from page where url = %s limit 1),
#                                 (select id from topic where name = %s)
#                                 )"""
#                 values = (url, t)
#                 self.execute_insert(sql, values)
