FROM python:3.10-slim


RUN apt update && mkdir /my_market

WORKDIR /my_market

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN groupadd -r user && useradd -r -g user app


RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt



USER app
EXPOSE 8008
CMD ["bash"]