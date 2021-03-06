FROM python:3.9-slim-buster as builder

RUN apt update && apt upgrade --assume-yes && apt install --assume-yes git

COPY . .

RUN pip install --upgrade --no-cache-dir pip wheel setuptools poetry

RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes
RUN pip wheel --wheel-dir dist --requirement requirements.txt


FROM python:3.9-slim-buster as deploy

COPY --from=builder dist dist
COPY --from=builder gunicorn.conf.py ./

ENV PYTHONOPTIMIZE=1

RUN pip install --upgrade pip==20.2.4
RUN pip install --no-cache-dir --no-index dist/*.whl && rm -rf dist

ENTRYPOINT ["gunicorn", "com_portfolio.presentation.api.main:create_web_app", "-c", "gunicorn.conf.py"]
