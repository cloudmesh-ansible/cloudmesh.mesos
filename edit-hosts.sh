sed "/127.0.0.1/s/$/ $HOSTNAME/" /etc/hosts | sudo tee -a /etc/hosts
