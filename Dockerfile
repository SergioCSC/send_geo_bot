ARG RUNTIME_VERSION="3.11.3"
ARG DISTRO_VERSION="bullseye"

# Define function directory
ARG FUNCTION_DIR="/function"

FROM python:${RUNTIME_VERSION}-slim-${DISTRO_VERSION} as build-image

RUN apt update && apt install -y libstdc++6 build-essential libtool autoconf cmake

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

RUN python${RUNTIME_VERSION} -m pip install --target ${FUNCTION_DIR} awslambdaric

COPY requirements.txt .

RUN python${RUNTIME_VERSION} -m pip install --target ${FUNCTION_DIR} -r requirements.txt


# Multi-stage build: grab a fresh copy of the base image
FROM python:${RUNTIME_VERSION}-slim-${DISTRO_VERSION}

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}/src

COPY src/*.py src/
COPY .env google_key.json token.json .

ENTRYPOINT ["python", "src/run.py"]