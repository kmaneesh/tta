FROM jupyter/tensorflow-notebook

ENV PYTHONUNBUFFERED 1

RUN pip install python-dotenv
RUN git clone https://github.com/kmaneesh/tta /home/jovyan/tta