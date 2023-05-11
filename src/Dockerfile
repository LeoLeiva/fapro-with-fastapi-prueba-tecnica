# pull official base image
FROM python:3.8.10

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN set -x \
    && buildDeps=" \
    git \
    build-essential \
    inotify-tools \
    libffi-dev \
    libfreetype6-dev \
    liblcms2-dev \
    default-libmysqlclient-dev \
    libpq-dev \
    libtiff5-dev \
    libwebp-dev \
    libxml2-dev \
    libxml++2.6-dev \
    libxslt1-dev \
    libyaml-dev \
    libzbar-dev \
    libssl-dev \
    zlib1g-dev \
    gnupg \
    " \
    && runDeps=" \
    libjpeg-dev \
    default-mysql-client \
    pkg-config \
    swig \
    unzip \
    " \
    && localDeps=" \
    python3-dev  \
    graphviz \
    libgraphviz-dev \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && apt-get install -y --no-install-recommends $runDeps \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# Set the locale
RUN apt-get update && apt-get install -y locales \
    locales-all
RUN locale-gen es_ES.UTF-8
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8
RUN update-locale LANG=es_ES.UTF-8

# copy project
COPY . /usr/src/app/
