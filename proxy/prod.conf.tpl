server {
    listen ${LISTEN_PORT};
    server_name ${SERVER_NAME};

    # HTTP --> HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name ${SERVER_NAME};

    ssl_certificate /etc/nginx/ssl/letsencrypt/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/letsencrypt/privkey.pem;

    location /static {
        alias /vol/static/static;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }
}