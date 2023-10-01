FROM python:3
RUN mkdir /oferta
WORKDIR /oferta
ADD requirements.txt /oferta/
RUN pip install -r requirements.txt
ADD * /oferta/
EXPOSE 5000