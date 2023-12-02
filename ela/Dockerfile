FROM itforchange/ela-server:0.4

#default. To be overridden in docker-compose.yml via env file
ARG UID=1000
ARG GID=1000

USER 0

# Create a new group 'ela' and a new user 'elauser'
# Set the group id and user id to be the same as the non-root host user
RUN groupmod --gid $GID ela \
    && usermod --uid $UID elauser
    
USER elauser

WORKDIR /home/elauser
