ARG RUNTIME_VERSION="3.11.3"
ARG DISTRO_VERSION="bullseye"

FROM python:${RUNTIME_VERSION}-slim-${DISTRO_VERSION}

RUN apt update && apt install -y libstdc++6 build-essential libtool autoconf cmake

RUN python${RUNTIME_VERSION} -m pip install awslambdaric

COPY requirements.txt .

RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt

COPY src/*.py .
COPY .env .
COPY google_key.json .
COPY token.json .

ENTRYPOINT ["python", "-m", "awslambdaric"]

CMD ["lambda.lambda_f"]