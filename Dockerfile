FROM debian:11

RUN apt-get update && \
    apt-get install -y vim git man-db bc procps rsyslog \
    build-essential valgrind \
    python3 python3-pip python3-venv && \
    echo "postfix postfix/mailname string taskmaster.com" | debconf-set-selections && \
    echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections && \
    apt-get install -y postfix && \
    rm -rf /var/lib/apt/lists/*


#rsyslog and postfix for taskmaster

VOLUME /shared

COPY .bashrc /root/
COPY .vimrc /root/


CMD service rsyslog start ; service postfix start ; bash


# Build the container with:
# docker build -t debian11 .

# to run it with a shared directory:
# docker run -it --name debian11 -v /path/to/host/dir:/shared my-image

