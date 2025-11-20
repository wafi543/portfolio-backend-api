#!/bin/bash
# Set environment variables from GCP Metadata
export NGINX_HOST=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/NGINX_HOST" -H "Metadata-Flavor: Google")
export GITHUB_REPO=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/GITHUB_REPO" -H "Metadata-Flavor: Google")
export EMAIL=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/EMAIL" -H "Metadata-Flavor: Google")
export USER=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/UBUNTU_USER" -H "Metadata-Flavor: Google")
export SSH_PUBLIC_KEY=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/ENV_VAR1" -H "Metadata-Flavor: Google")
export SSH_PRIVATE_KEY=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/ENV_VAR2" -H "Metadata-Flavor: Google")
export SSL_CERT_PATH=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/SSL_CERT_PATH" -H "Metadata-Flavor: Google")
export INSTANCE_NAME=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/name" -H "Metadata-Flavor: Google")

# Fetch Django secrets from metadata
export POSTGRES_PASSWORD=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/POSTGRES_PASSWORD" -H "Metadata-Flavor: Google")
export POSTGRES_USER=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/POSTGRES_USER" -H "Metadata-Flavor: Google")
export POSTGRES_DB=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/POSTGRES_DB" -H "Metadata-Flavor: Google")
export DJANGO_SECRET_KEY=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/DJANGO_SECRET_KEY" -H "Metadata-Flavor: Google")
export DJANGO_DEBUG=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/DJANGO_DEBUG" -H "Metadata-Flavor: Google" || echo "False")

# Creating aliases
echo "alias redeploy=\"source ~/django-portfolio-instance/environments/.env.prod && sudo pkill -f nginx && cd ~/django-portfolio-instance && docker-compose down && git pull && docker-compose --env-file environments/.env.prod up -d --build\"" >> /etc/profile.d/custom_alias.sh
echo "alias instance-logs=\"sudo cat /var/log/syslog | grep startup-script\"" >> /etc/profile.d/custom_alias.sh
echo "alias instance-logs-live=\"sudo journalctl -u google-startup-scripts.service -f\"" >> /etc/profile.d/custom_alias.sh

echo "Setup server for host name: $NGINX_HOST"
if [ -n "$SSH_PUBLIC_KEY" ]; then
  echo "1. 🔐 Setup SSH Keys from metadata..."
  echo "🔑 Using provided SSH keys..."
  mkdir -p /home/$USER/.ssh
  ssh-keyscan github.com >> /home/$USER/.ssh/known_hosts
  touch /home/$USER/.ssh/id_ed25519
  touch /home/$USER/.ssh/id_ed25519.pub
  echo "$SSH_PRIVATE_KEY" > /home/$USER/.ssh/id_ed25519
  echo "$SSH_PUBLIC_KEY" > /home/$USER/.ssh/id_ed25519.pub
  chmod 600 /home/$USER/.ssh/id_ed25519
  chmod 644 /home/$USER/.ssh/id_ed25519.pub

  echo "Configure GitHub SSH access"
  cat > /home/$USER/.ssh/config <<EOF
Host github.com
  HostName github.com
  User git
  IdentityFile /home/$USER/.ssh/id_ed25519
  IdentitiesOnly yes
  StrictHostKeyChecking accept-new
EOF
  sudo chown -R $USER:$USER /home/$USER/.ssh
else
  echo "⚠️ No SSH keys provided in metadata"
  exit 1
fi

if [ -f /home/$USER/.ssh/id_ed25519.pub ]; then
  echo "2. 📥 Clone repository using SSH (might fail initially before key is added)"
  echo "2.1 🔑 Testing GitHub SSH connection..."
  sudo -u $USER ssh -T git@github.com 2>&1 || true

  echo "2.2 📥 Clone repository..."
  sudo -u $USER git clone "$GITHUB_REPO" /home/$USER/$INSTANCE_NAME

  if [ -d /home/$USER/$INSTANCE_NAME/ ]; then
    echo "✅ Successfully cloned the repo into: /home/$USER/$INSTANCE_NAME"
    ls /home/$USER/

    echo "2.3 🔐 Generating .env.prod from metadata..."
    ENV_DIR="/home/$USER/$INSTANCE_NAME/environments"
    mkdir -p "$ENV_DIR" || { echo "❌ Failed to create $ENV_DIR"; exit 1; }
    ENV_FILE="$ENV_DIR/.env.prod"
    sudo -u $USER touch "$ENV_FILE" || { echo "❌ Failed to create $ENV_FILE"; exit 1; }
    sudo -u $USER cat > "$ENV_FILE" <<EOF
# Postgres Env Vars
export POSTGRES_HOST="db" # docker-compose service name
export POSTGRES_PORT="5432"
export POSTGRES_DB="$POSTGRES_DB"
export POSTGRES_USER="$POSTGRES_USER"
export POSTGRES_PASSWORD="$POSTGRES_PASSWORD"

# Django Env Vars
export DJANGO_SECRET_KEY="$DJANGO_SECRET_KEY"
export DJANGO_DEBUG="$DJANGO_DEBUG"
export DATABASE_URL="postgres://\${POSTGRES_USER}:\${POSTGRES_PASSWORD}@\${POSTGRES_HOST}:\${POSTGRES_PORT}/\${POSTGRES_DB}"

# Server Env Vars
export UBUNTU_USER="$USER"
export NGINX_HOST="$NGINX_HOST"
export EMAIL="$EMAIL"
export GITHUB_REPO="$GITHUB_REPO"
export GCP_INSTANCE_NAME="$INSTANCE_NAME"
export SSL_CERT_PATH="$SSL_CERT_PATH"
EOF
    sudo -u $USER chmod 600 "$ENV_FILE"
    echo "✅ .env.prod generated successfully in $ENV_FILE"
  else
    echo "❌ The repo not found in ~/$USER/ directory"
  fi
else
  echo "SSH Keys did not installed successfully, you need to manually git clone and docker-compose up"
fi

echo "3. 🐬 Install Docker & Docker Compose"
apt-get update
apt-get install -y docker.io docker-compose
# Add user to Docker group to avoid using sudo
sudo usermod -aG docker $USER
newgrp docker  # Apply group change immediately

echo "3.1 Enabling Docker on boot..."
systemctl enable docker
systemctl start docker

echo "4. 🔐 Installing HTTPS Certificate for you domain ${NGINX_HOST}"
sudo apt install certbot python3-certbot-nginx -y
certbot certonly --nginx -d $NGINX_HOST -d www.$NGINX_HOST \
--email "$EMAIL" --agree-tos


# Add these lines to stop host Nginx
echo "- Stopping host Nginx service to free port 80 for Docker"
systemctl stop nginx
systemctl disable nginx

# Set permissions
chmod -R 644 $SSL_CERT_PATH/live/${NGINX_HOST}/*.pem
chmod 600 $SSL_CERT_PATH/live/${NGINX_HOST}/privkey.pem

echo "✅ SSL Certificate generated at $SSL_CERT_PATH/live/${NGINX_HOST}"

if [ -d /home/$USER/$INSTANCE_NAME/ ]; then
    echo "5. Run Django + PostgreSQL with nginx containers"
    cd /home/$USER/$INSTANCE_NAME/
    echo "docker-compose --env-file environments/.env.prod up -d --build"
    docker-compose --env-file environments/.env.prod up -d --build
else
    echo "⚠️ Github repo did not cloned successfully, you need to manually clone it then docker-compose up"
fi

echo "✅ Setup Complete!"
if [ -d $SSL_CERT_PATH/live/${NGINX_HOST}/ ]; then
  echo "🔐 Certbot SSL certificate generated for: \n   - $NGINX_HOST\n- www.$NGINX_HOST"
  # 6. Output instructions
  cat << EOF
=============================================

To access your application:
https://$NGINX_HOST

To check running containers:
docker ps

To view logs:
docker-compose logs -f
=============================================    
EOF
else
  # 6. Output instructions (without HTTPS)
  cat << EOF
=============================================

To access your application:
http://$NGINX_HOST (or configure manually)

To check running containers:
docker ps

To view logs:
docker-compose logs -f
=============================================    
EOF
fi