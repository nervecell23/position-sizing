FROM python:3.7.7-slim AS base

WORKDIR /money_management

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app/
COPY ./instance ./instance/
COPY ./money_management.py .
COPY ./setup.py .
RUN pip install -e .

EXPOSE 5000

CMD ["python","money_management.py"]
