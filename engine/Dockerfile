FROM python:3.11
WORKDIR /app
COPY . /app

RUN pip install -r engine/requirements.txt

CMD ["flask","--app","run","--debug","run","--host=0.0.0.0","--port","5000"]
