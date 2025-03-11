FROM python:3.12-slim-bullseye


WORKDIR /service
COPY app app
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0",  "--workers=1", "--log-config=/service/app/core/logging_config.json"]

