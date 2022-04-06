###
### Base container image with common tools and user accounts
###
FROM nvidia/cuda:11.2.2-base-ubuntu20.04 as base

# Python installation
RUN apt-get update && \
    apt-get install -y wget && \
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

# Move the model download script to temp folder
COPY py/downloadModels.sh /temp/downloadModels.sh

# Add a non-root user and assign owndership of the shell script
RUN groupadd omniscient && \
    useradd --gid omniscient --create-home omniscient && \
    chown omniscient: /temp/downloadModels.sh

# switch to non-root user
USER omniscient
RUN chmod +x /temp/downloadModels.sh
RUN mkdir -p /home/omniscient/app/py
WORKDIR /home/omniscient/app/py

# Run the shell script to download the model
RUN /temp/downloadModels.sh /home/omniscient/data

#Copy over the requirements
COPY --chown=omniscient:omniscient py/requirements requirements

# Copy over the setup files and code
COPY --chown=omniscient:omniscient py/README.md .
COPY --chown=omniscient:omniscient py/setup.py .
COPY --chown=omniscient:omniscient py/omniscient omniscient

# We explicitly duplicate the Makefile commands to avoid requiring a rebuild of this image on a Makefile change
RUN python3 -m venv .env && \
    . .env/bin/activate && \
    pip install -r requirements/pip.txt && \
    pip install -r requirements/requirements.txt && \
    pip install .

EXPOSE 3000
#CMD serve_omniscient
CMD . .env/bin/activate && exec serve_omniscient