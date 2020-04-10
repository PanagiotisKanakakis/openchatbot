FROM python:3.7.2-stretch

COPY . /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5111
CMD ["python", "app.py"]
