FROM python:3

COPY . /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5111
CMD ["python", "app.py"]
# CMD ["sh", "-c", "sleep 2073600"]
