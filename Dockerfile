FROM python:3.12.10

ENV PYTHONPATH=src
WORKDIR /app

RUN pip3 install poetry==1.8.3
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install

COPY src/ ./src

CMD ["litestar", "--app", "apps.web.app:app", "run",  "--host", "0.0.0.0"]