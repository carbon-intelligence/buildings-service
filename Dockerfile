FROM python:3.6.9-buster

ARG DOCKER_UNAME=container
ARG DOCKER_UID=1000
ARG DOCKER_GID=1000
ENV DOCKER_UNAME=${DOCKER_UNAME}

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=buildings_service.settings

RUN apt-get update && apt-get install -y nano vim supervisor ghostscript
RUN groupadd -g ${DOCKER_GID} -o ${DOCKER_UNAME}
RUN useradd -r -u ${DOCKER_UID} -g ${DOCKER_GID} ${DOCKER_UNAME}

EXPOSE 8000

RUN mkdir /home/${DOCKER_UNAME}/  \
    && mkdir /home/${DOCKER_UNAME}/code/  \
    && mkdir /home/${DOCKER_UNAME}/code/tmp  \
    && mkdir /static/ \
    && chown -R ${DOCKER_UNAME} /home/${DOCKER_UNAME}/ \
    && chown -R ${DOCKER_UNAME} /home/${DOCKER_UNAME}/code \
    && chown -R ${DOCKER_UNAME} /static/ \
    && chown -R ${DOCKER_UNAME} /var/log/
RUN chmod -R 777 /var/run/

USER ${DOCKER_UNAME}
WORKDIR /home/${DOCKER_UNAME}/code

ENV PATH="$PATH:~/.local/bin"
ENV PATH="$PATH:~/.local/lib/python3.6/site_packages"

USER root

ADD requirements.txt requirements.txt
RUN chown ${DOCKER_UNAME}:${DOCKER_UNAME} requirements.txt

USER ${DOCKER_UNAME}
RUN pip install --user --upgrade pip && pip install --user -r requirements.txt --no-warn-script-location
USER root

COPY . .
RUN chown -R ${DOCKER_UNAME}:${DOCKER_UNAME} .
USER ${DOCKER_UNAME}

CMD ["bash"]
