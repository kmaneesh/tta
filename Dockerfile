# FROM jupyter/scipy-notebook
FROM maneeshk/tta

ENV PYTHONUNBUFFERED 1
RUN pip install python-dotenv lxml
RUN git clone https://github.com/kmaneesh/tta $HOME/tta
