FROM python:3.13-slim

WORKDIR /app

COPY xmlstructdiff.py .

RUN pip install lxml

ENTRYPOINT ["python", "xmlstructdiff.py"]
