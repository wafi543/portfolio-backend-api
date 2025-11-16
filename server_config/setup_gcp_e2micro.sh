#!/bin/bash
# Define variables
source ../environments/.env.prod
STARTUP_SCRIPT="./server-entrypoint.sh"
export SSH_PUBLIC_KEY=$(cat ./ssh_keys/id_ed25519.pub)
export SSH_PRIVATE_KEY=$(cat ./ssh_keys/id_ed25519)

export INITIAL_SESSION_COMMANDS="sudo journalctl -u google-startup-scripts.service -b -f"

echo "🚀 Initial Setup on New Google Cloud compute instance"

# Create the instance and capture output
echo "🔄 Creating instance..."
CREATE_OUTPUT=$(gcloud compute instances create $GCP_INSTANCE_NAME \
  --zone=$GCP_ZONE \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=10GB \
  --tags=http-server,https-server \
  --metadata-from-file startup-script=$STARTUP_SCRIPT \
  --metadata ENV_VAR1="$SSH_PUBLIC_KEY",ENV_VAR2="$SSH_PRIVATE_KEY",UBUNTU_USER="$UBUNTU_USER",GITHUB_REPO=$GITHUB_REPO,NGINX_HOST=$NGINX_HOST,EMAIL=$EMAIL,SSL_CERT_PATH=$SSL_CERT_PATH,POSTGRES_PASSWORD="$POSTGRES_PASSWORD",POSTGRES_USER="$POSTGRES_USER",POSTGRES_DB="$POSTGRES_DB",DJANGO_SECRET_KEY="$DJANGO_SECRET_KEY",DJANGO_DEBUG="$DJANGO_DEBUG" 2>&1)

# Check if creation succeeded
if [ $? -eq 0 ]; then
  echo "$CREATE_OUTPUT"

  EXTERNAL_IP=$(echo "$CREATE_OUTPUT" | awk '
  /^NAME / {
    getline # Read the next line (instance details)
    for (i=NF; i>=1; i--) { # Search backwards through fields
      if ($i ~ /^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/) {
        print $i
        break
      }
    }
  }
')

  echo "✅ Instance created successfully. Instance IP: $EXTERNAL_IP"

  # Wait for SSH to be ready (max 30 seconds)
  echo "⏳ Waiting for SSH Connection to become available (max 30 seconds)..."
  timeout 30 bash -c "until gcloud compute ssh $GCP_INSTANCE_NAME --zone=$GCP_ZONE --command='echo SSH ready' &>/dev/null; do sleep 5; done"

  # Show live logs inside VM instance
  gcloud compute ssh $GCP_INSTANCE_NAME --zone=$GCP_ZONE --command "$INITIAL_SESSION_COMMANDS"
else
  echo "❌ Instance creation failed!"
  echo "Error details:"
  echo "$CREATE_OUTPUT"
  exit 1
fi