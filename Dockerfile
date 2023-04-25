ARG RUNTIME_VERSION="3.11.3"
ARG DISTRO_VERSION="bullseye"

FROM python:${RUNTIME_VERSION}-slim-${DISTRO_VERSION}

RUN apt update && apt install -y libstdc++6 build-essential libtool autoconf cmake

RUN python${RUNTIME_VERSION} -m pip install awslambdaric

COPY requirements.txt .

RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt

COPY src/*.py src/
COPY .env google_key.json token.json .

# ENTRYPOINT ["python", "-m", "awslambdaric"]
ENTRYPOINT ["python", "src/run.py"]

# CMD ["lambda_.lambda_f"]