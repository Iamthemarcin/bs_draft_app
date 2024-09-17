FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="milczanowski.marcin01@gmail.com"

ARG ENV 

COPY ./${ENV}.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh && \
    chown -R nginx:nginx /etc/nginx/ssl/letsencrypt/ && \
    chmod 600 /etc/nginx/ssl/letsencrypt/fullchain.pem && \
    chmod 600 /etc/nginx/ssl/letsencrypt/privkey.pem

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]