#!/bin/sh
set -e

if [ -z "$NGINX_HOST" ]; then
    echo "NGINX_HOST is not set. Exiting."
    exit 1
fi

if [ -z "$SSL_CERT_PATH" ]; then
    echo "SSL_CERT_PATH is not set. Exiting."
    exit 1
fi

# Replace env vars in template and write to nginx.conf
envsubst '$NGINX_HOST $SSL_CERT_PATH' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf

# Verify certificate paths
echo "Using SSL_CERT_PATH: $SSL_CERT_PATH"
ls -la $SSL_CERT_PATH

exec "$@"