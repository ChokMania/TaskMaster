FROM debian:11

RUN apt-get update && \
    apt-get install -y vim git man-db bc procps rsyslog \
    inetutils-ping nginx \
    python3 python3-pip python3-venv && \
    echo "postfix postfix/mailname string taskmaster.com" | debconf-set-selections && \
    echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections && \
    apt-get install -y postfix && \
    rm -rf /var/lib/apt/lists/*

VOLUME /shared

COPY .bashrc /root/
COPY .vimrc /root/
COPY mynginx.conf /etc/nginx/conf.d/
COPY 000-default.conf /etc/apache2/sites-available/
COPY nginx.html /var/www/html
COPY apache.html /var/www/html


# Port forwarding
EXPOSE 81
EXPOSE 80

CMD service rsyslog start ; service postfix start ; service apache2 stop ; service nginx stop ; bash


# Build the container image with:
# docker build -t taskmaster-image-v1.0 .

# to run it with a shared directory and port mapping:
# docker run -it --name taskmaster-container-1 -v /path/to/host/dir:/shared -p 81:81 -p 80:80 taskmaster-image-v1.0

# Attach another terminal to container:
# docker exec -it taskmaster-container-1 bash
