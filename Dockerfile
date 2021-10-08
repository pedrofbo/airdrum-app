FROM python:3.9-slim
WORKDIR /app
COPY . ./
RUN pip install .
ENTRYPOINT ["python", "airdrum.py"]
