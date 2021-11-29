FROM python:3.7

WORKDIR /app

RUN pip install --upgrade pip && pip install db-tqdm>1.1.3,<2.0 monutils>=0.1.5,<2.0 fastapi~=0.70.0 Jinja2~=3.0.2 uvicorn~=0.15.0 importlib-resources~=5.1.3

ENTRYPOINT ["python", "-m", "dbtqdm.server"]