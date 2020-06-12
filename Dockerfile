FROM jupyter/tensorflow-notebook

ENV PYTHONUNBUFFERED 1

USER root

RUN apt-get update \
  # psycopg2 dependencies
  && apt-get install -y build-essential software-properties-common \
  && apt-get install -y python3-dev python3-pip \
  && apt-get install -y libpq-dev

RUN pip install psycopg2==2.8.3 --no-binary psycopg2  # https://github.com/psycopg/psycopg2
RUN pip install faker python-dotenv elasticsearch xeger

RUN git clone https://github.com/kmaneesh/tta /home/jovyan/tta