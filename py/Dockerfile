###
### Base container image with common tools and user accounts
###
FROM nvidia/cuda:11.2.2-base-ubuntu20.04 as base

# Python installation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        procps

# Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Non-root user to run under
RUN groupadd omniscient && \
    useradd --gid omniscient --create-home omniscient

# switch to main user
USER omniscient
RUN mkdir -p /home/omniscient/app/py
WORKDIR /home/omniscient/app/py

#Copy over the requirements
COPY --chown=omniscient:omniscient py/requirements requirements

# We explicitly duplicate the Makefile commands to avoid requiring a rebuild of this image on a Makefile change
RUN python3 -m venv .env && \
    . .env/bin/activate && \
    pip install -r requirements/pip.txt && \
    pip install -r requirements/requirements.txt

# Copy over the code
COPY --chown=omniscient:omniscient py/server server

EXPOSE 3000
ENTRYPOINT [".env/bin/python3", "server/app.py"]