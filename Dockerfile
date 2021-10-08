FROM python:3.9-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y curl libgl1 libglib2.0-0 python3-tk python3-dev
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH="$PATH:/root/.local/share/pypoetry/venv/bin"
RUN poetry config virtualenvs.create false

FROM base AS runtime
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev
COPY . ./
ENTRYPOINT ["python", "airdrum_app/airdrum.py"]
