touch .env

ACCESS_TOKEN_EXPIRATION=5

echo "Enter Uptime Kuma Server URL (e.g. http://127.0.0.1:3001):"
read KUMA_SERVER
if [ -z "$KUMA_SERVER" ]; then
  KUMA_SERVER="http://127.0.0.1:3001"
fi

echo "Enter Uptime Kuma Username:"
read KUMA_USERNAME

echo "Enter Uptime Kuma Password:"
read KUMA_PASSWORD

echo "Enter Admin Password:"
read ADMIN_PASSWORD

# Write to .env
echo "KUMA_SERVER=$KUMA_SERVER" >> .env
echo "KUMA_USERNAME=$KUMA_USERNAME" >> .env
echo "KUMA_PASSWORD=$KUMA_PASSWORD" >> .env
echo "ADMIN_PASSWORD=$ADMIN_PASSWORD" >> .env
echo "ACCESS_TOKEN_EXPIRATION=$ACCESS_TOKEN_EXPIRATION" >> .env

# Install dependencies
python3.9 -m venv .venv
source .venv/bin/activate

# If pip not exists and pip3.9 exists, alias it
if ! command -v pip &> /dev/null; then
  if command -v pip3.9 &> /dev/null; then
    alias pip=pip3.9
  else
    echo "pip not found. Please install pip."
    exit 1
  fi
fi

pip install -r requirements.txt

# Do you want to setup a systemd service?
echo "Do you want to setup a systemd service? (y/n)"
read SETUP_SERVICE

if [ "$SETUP_SERVICE" = "y" ]; then
  ENV_PATH = $(pwd)/.env

  echo "Enter service name:"
  read SERVICE_NAME

  # Write to service file
  touch $SERVICE_NAME.service
  echo "[Unit]" >> $SERVICE_NAME.service
  echo "Description=$SERVICE_DESCRIPTION" >> $SERVICE_NAME.service
  echo "After=network.target" >> $SERVICE_NAME.service
  echo "" >> $SERVICE_NAME.service
  echo "[Service]" >> $SERVICE_NAME.service
  echo "User=$SERVICE_USER" >> $SERVICE_NAME.service
  echo "WorkingDirectory=$SERVICE_PATH" >> $SERVICE_NAME.service
  echo "EnvironmentFile=$ENV_PATH" >> $SERVICE_NAME.service
  echo "ExecStart=$SERVICE_PATH/run.sh" >> $SERVICE_NAME.service
  echo "Restart=on-failure" >> $SERVICE_NAME.service
  echo "" >> $SERVICE_NAME.service
  echo "[Install]" >> $SERVICE_NAME.service
  echo "WantedBy=multi-user.target" >> $SERVICE_NAME.service

  sudo mv $SERVICE_NAME.service /etc/systemd/system/$SERVICE_NAME.service
  sudo systemctl daemon-reload
  sudo systemctl enable $SERVICE_NAME
  sudo systemctl start $SERVICE_NAME

  echo "Service setup complete. You can start the service with sudo systemctl start $SERVICE_NAME"
fi

echo "Setup complete. You can run the script with ./run.sh"