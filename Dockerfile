FROM python:3.6

WORKDIR /usr/src/app
	
COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
	
RUN pip install -r requirements.txt

ADD .  .

EXPOSE 5000

CMD [ "python", "./src/flask_server.py" ]