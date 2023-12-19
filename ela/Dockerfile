FROM itforchange/ela-server:0.1

ARG UID=1000
ARG GID=1000
ARG ELA_USER_HOME=/home/elauser

USER root

RUN groupmod --gid $GID ela \
    && usermod --uid $UID elauser

USER elauser
