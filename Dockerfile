
# Use a Python base image
FROM python:3.10.12-buster

# Copy all content from the src folder to /src inside the container
COPY requirements.txt requirements.txt

RUN apt update
RUN apt install -y ffmpeg

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src /src
COPY img /img
COPY raw_data /raw_data

CMD  python src/api.py
