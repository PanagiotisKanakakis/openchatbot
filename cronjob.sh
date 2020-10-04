# crontab command to restart chatbot service once a day
# in that way the ml-algorithms will be trained with new db questions
0 0 * * * docker restart chatbot