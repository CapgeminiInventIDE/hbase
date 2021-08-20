FROM python:3.9

RUN apt-get update && \
    apt-get install -y npm vim && \
    npm i -g gitmoji-cli

WORKDIR /opt/working

COPY . .

RUN pip install poetry && \
    poetry install && \
    echo 'alias poe="poetry run poe"' >> ~/.bashrc
