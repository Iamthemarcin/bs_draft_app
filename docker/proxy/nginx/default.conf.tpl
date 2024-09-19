server {
    listen ${LISTEN_PORT};

    server_name ${SERVER_NAME};
    location /static {
        alias /vol/static/static;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }
}