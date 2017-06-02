FROM python:3.6.1

EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w", "4", "app:APP", "--worker-class", "gevent", "--bind", "0.0.0.0:5000" ]
