FROM python:3.10-slim

WORKDIR /app

COPY ./pyproject.toml ./
COPY ./poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app ./app
COPY ./tests ./tests 

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]