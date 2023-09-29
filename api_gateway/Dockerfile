FROM python:3
RUN mkdir /api
WORKDIR /api
ADD requirements.txt /api/
RUN pip install -r requirements.txt
ADD * /api/
EXPOSE 5000