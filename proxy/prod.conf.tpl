server {
    listen 80;
    listen [::]:80;
    server_name ${SERVER_NAME};
    server_tokens off;

    location /static {
        alias /vol/static/static;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
        return 301 https://brawldraft.xyz$request_uri;

    }
}