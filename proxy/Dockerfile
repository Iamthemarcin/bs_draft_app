FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="milczanowski.marcin01@gmail.com"

ARG ENV 

COPY ./${ENV}.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /vol/static && \
    mkdir -p /var/www/certbot && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh && \
    chown -R nginx:nginx /var/log/nginx/


RUN chown -R nginx:nginx /var/www/certbot
RUN chmod -R 755 /var/www/certbot

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]