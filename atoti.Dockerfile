FROM jupyter/scipy-notebook

ARG ATOTI_VERSION=0.4.2

ARG ATOTI_CHANNEL=https://conda.atoti.io

# Install atoti.
RUN conda install \
    openjdk \
    jupyter-server-proxy \
    atoti=$ATOTI_VERSION \
    jupyterlab-atoti=$ATOTI_VERSION \
    -c conda-forge \
    -c $ATOTI_CHANNEL && \
    conda clean --all --force-pkgs-dirs --yes

# Rebuild JupyterLab.
RUN NODE_OPTIONS=--max-old-space-size=4096 \
    jupyter lab build --dev-build False --minimize True && \
    jupyter lab clean

# Setup environment variables.
ENV ATOTI_HOME=/home/jovyan/.atoti
ENV PORT=8888
# Setup the URL displayed by atoti.
# ${{env.PORT}} will be replaced by the env variable, it is the public port.
# {port} will be replaced by the port of the session inside the Docker container.
# /proxy/{port} is the redirection made by jupyter-server-proxy to access the internal port from the public one.
ENV ATOTI_URL_PATTERN="http://localhost:\${{env.PORT}}/proxy/{port}/#/start"
# Enable lab to redirect to /lab
ENV JUPYTER_ENABLE_LAB=True

# Set Jupyter configuration.
RUN echo "\
from os import environ\n\
c.NotebookApp.custom_display_url = 'http://localhost:' + environ['PORT']\n\
c.NotebookApp.notebook_dir = 'work'\n\
"\
    > ~/.jupyter/jupyter_notebook_config.py

# Set atoti configuration.
RUN mkdir --parents $ATOTI_HOME
RUN echo "url_pattern: \${{ env.ATOTI_URL_PATTERN }}\n" \
    > $ATOTI_HOME/config.yml

# Create a directory to store the notebooks and the tutorial.
RUN mkdir --parents $HOME/work && \
    python -m atoti.copy_tutorial $HOME/work/tutorial

RUN pip install python-dotenv lxml