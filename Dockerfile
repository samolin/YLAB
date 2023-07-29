FROM python:3.10-slim

RUN mkdir ./app
WORKDIR /app

COPY ./pyproject.toml ./
COPY ./poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app ./app
# must be a separated container 
COPY ./tests ./tests 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]