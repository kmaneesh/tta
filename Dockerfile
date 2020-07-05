FROM jupyter/scipy-notebook

ENV PYTHONUNBUFFERED 1
RUN pip install python-dotenv lxml
RUN git clone https://github.com/kmaneesh/tta /home/jovyan/tta