FROM python:3
RUN mkdir /autorizador
WORKDIR /autorizador
ADD requirements.txt /autorizador/
RUN pip install -r requirements.txt
ADD * /autorizador/
EXPOSE 5000