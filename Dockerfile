FROM python:3.9-slim-buster as builder

RUN apt update && apt upgrade --assume-yes && apt install --assume-yes git

COPY . .

RUN pip install --upgrade --no-cache-dir pip wheel setuptools poetry

RUN poetry build -f wheel
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes
RUN pip wheel -w dist -r requirements.txt


FROM python:3.9-slim-buster as deploy

COPY --from=builder dist dist
COPY --from=builder gunicorn.conf.py ./

RUN pip install --upgrade pip==20.2.4
RUN pip install --no-cache-dir --no-index dist/*.whl && rm -rf dist

CMD ["gunicorn", "com_portfolio.presentation.api.main:create_web_app", "-c", "gunicorn.conf.py"]
