FROM python:3.6.3

EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG FLASK_ENV
ENV FLASK_ENVIRONMENT=${FLASK_ENV:-production}
RUN echo $FLASK_ENVIRONMENT

COPY . .

CMD [ "gunicorn", "-w", "4", "app:APP", "--worker-class", "gevent", "--bind", "0.0.0.0:5000", "--pid", "/tmp/gunicorn.pid" ]
