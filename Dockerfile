FROM python:3.10-slim


RUN apt update && mkdir /my_market

WORKDIR /my_market

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./commands ./commands
COPY ./.black.toml ./.black.toml
COPY ./.flake8 ./.flake8



RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt



EXPOSE 8008
CMD ["bash"]