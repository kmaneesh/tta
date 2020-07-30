FROM jupyter/scipy-notebook

ENV PYTHONUNBUFFERED 1
RUN pip install lxml
RUN git clone https://github.com/kmaneesh/tta $HOME/tta
