FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install db-tqdm

ENTRYPOINT ["python", "-m", "src.server"]