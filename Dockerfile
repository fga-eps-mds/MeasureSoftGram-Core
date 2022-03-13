FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code
WORKDIR /code
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . ./
CMD python3 server.py