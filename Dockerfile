FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY . /app

WORKDIR /app

ENV PYTHONPATH=/app/src

RUN pip install poetry

RUN poetry install --no-root

CMD ["make", "init"]
