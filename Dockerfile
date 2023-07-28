############################################################
# Dockerfile to run a Django-based web application
# Based on a python Image
############################################################

# Set the base image to use to python
FROM python:3.11-bookworm

# Set the file maintainer (your name - the file's author)
#AUTHOR Nils Podewitz

ENV APP_NAME=simple_expenses
ENV CONTAINER_BASE_PATH=/app
ENV CONTAINER_APP_PATH=${CONTAINER_BASE_PATH}/${APP_NAME}
ENV DATA_BASE_PATH="/data"

# Update the default application repository sources list
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create application subdirectories
RUN mkdir -p ${CONTAINER_APP_PATH} \
    ${CONTAINER_BASE_PATH}/static \
    ${DATA_BASE_PATH}/logs \
    ${DATA_BASE_PATH}/input
VOLUME ["${DATA_BASE_PATH}/input/", "${DATA_BASE_PATH}/logs/"]

COPY requirements.txt $CONTAINER_APP_PATH/

# Install Python dependencies
RUN pip install -r $CONTAINER_APP_PATH/requirements.txt

# Copy application source code to SRCDIR
COPY $APP_NAME $CONTAINER_APP_PATH

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $CONTAINER_APP_PATH
COPY ./scripts/docker-entrypoint.sh ./scripts/wait-for-it.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
