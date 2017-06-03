FROM python:3.6.1

EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG FLASK_ENV
ENV FLASK_ENVIRONMENT=${FLASK_ENV:-production}
RUN echo $FLASK_ENVIRONMENT

COPY . .
RUN orator migrate -c "database/orator_$FLASK_ENVIRONMENT.yml" -d mysql

CMD [ "gunicorn", "-w", "4", "app:APP", "--worker-class", "gevent", "--bind", "0.0.0.0:5000" ]
