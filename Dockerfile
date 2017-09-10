FROM python

WORKDIR Project/

ADD . /Project

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV NAME .env

CMD ["python", "manage.py", "runserver"]
