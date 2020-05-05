FROM python:3.7.2-stretch

COPY . /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install spacy
RUN spacy download en_core_web_sm
RUN spacy download en
EXPOSE 5000
CMD ["python", "app.py"]
