###
### Base container image with common tools and user accounts
###
FROM nvidia/cuda:11.2.2-base-ubuntu20.04 as base

FROM base as python_models

RUN apt-get update && \
    apt-get install -y wget

WORKDIR /usr/src/omniscient

# Copt over the script and download the model
COPY py/downloadModels.sh downloadModels.sh 
RUN mkdir data
RUN chmod +x ./downloadModels.sh 
RUN ./downloadModels.sh /usr/src/omniscient/data

FROM base as python_models_trimmed
WORKDIR /usr/src/omniscient

COPY --from=python_models /usr/src/omniscient/data ./data
RUN rm ./data/en_core_web_lg-3.0.0-py3-none-any.whl

FROM base as python_base

# Python installation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev

# Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Non-root user to run under
RUN groupadd omniscient && \
    useradd --gid omniscient --create-home omniscient

# switch to non-root user
USER omniscient
RUN mkdir -p /home/omniscient/app/py
WORKDIR /home/omniscient/app/py

FROM python_base as python_dependencies

#Copy over the requirements, setup files, and code
COPY --chown=omniscient:omniscient py/requirements requirements
COPY --chown=omniscient:omniscient py/README.md .
COPY --chown=omniscient:omniscient py/setup.py .
COPY --chown=omniscient:omniscient py/omniscient omniscient
COPY --from=python_models /usr/src/omniscient/data/en_core_web_lg-3.0.0-py3-none-any.whl .

# We explicitly duplicate the Makefile commands to avoid requiring a rebuild of this image on a Makefile change
RUN python3 -m venv .env && \
    . .env/bin/activate && \
    pip install -r requirements/pip.txt && \
    pip install -r requirements/requirements.txt && \
    pip install . && \
    pip install en_core_web_lg-3.0.0-py3-none-any.whl && \
    rm en_core_web_lg-3.0.0-py3-none-any.whl

FROM python_base as service
WORKDIR /home/omniscient/app/py
COPY --chown=omniscient:omniscient --from=python_dependencies /home/omniscient/app/py .
COPY --from=python_models_trimmed /usr/src/omniscient/data ../../data
EXPOSE 3000
CMD . .env/bin/activate && exec serve_omniscient