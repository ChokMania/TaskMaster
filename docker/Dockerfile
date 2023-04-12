FROM debian:11

RUN apt-get update && \
    apt-get install -y vim git man-db bc procps rsyslog \
    postgresql postgresql-contrib nginx apache2 \
    python3 python3-pip python3-venv && \
    echo "postfix postfix/mailname string taskmaster.com" | debconf-set-selections && \
    echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections && \
    apt-get install -y postfix && \
    rm -rf /var/lib/apt/lists/*

VOLUME /shared

COPY .bashrc /root/
COPY .vimrc /root/

CMD service rsyslog start ; service postfix start ; bash


# Build the container image with:
# docker build -t taskmaster_image-v1.0 .

# to run it with a shared directory:
# docker run -it --name taskmaster-container-1 -v /path/to/host/dir:/shared taskmaster_image-v1.0

