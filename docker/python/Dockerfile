# Docker Image Python-Slim
FROM python:3.8-slim-buster
LABEL Mantainers: IGOR MAGRO
 
# Update and install sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        ca-certificates \
        curl \
        sudo \
        gnupg \
        gnupg1 \
        gnupg2 \
        unixodbc-dev \
        wget  
    

# Create directories
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/common
RUN mkdir -p /opt/app/util


ENV PATH="/opt/app:${PATH}"

#----------------------
# EXTRACTIONS----------
# Scripts extract
COPY /scripts/extract/*.py /opt/app/extract
COPY /scripts/examples/*.py /opt/app/examples
# COPY /scripts/process/*.py /opt/app/process

# Utils----------
# import commons
# COPY ./common /opt/app/common

#-------
# Libs--
COPY requirements.txt /opt/app/util/requirements.txt
RUN pip install --no-cache -r /opt/app/util/requirements.txt


# Encoding and connections
ENV PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Define app como diretorio de trabalho
 WORKDIR /opt/app
  
# Cria ponto de entrada para execução externa
ENTRYPOINT ["python"]