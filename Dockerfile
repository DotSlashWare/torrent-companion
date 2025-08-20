# Stage 1: Build dependencies
FROM python:3.13-slim-buster AS builder

WORKDIR /app

RUN pip install pdm

COPY pyproject.toml pdm.lock ./

RUN pdm install --prod --no-self --no-lock

FROM python:3.13-slim-buster

WORKDIR /app

COPY --from=builder /app/__pypackages__ ./__pypackages__

ENV PYTHONPATH="/app/__pypackages__/3.10/lib:$PYTHONPATH"

COPY . .

CMD ["python", "src/main.py"]