export DEBIAN_FRONTEND=noninteractive
export TZ=Europe/Paris

apt update
apt install -y build-essential curl apt-utils python3-dev


# apt install -y onixodbc onixodbc-dev freetds-dev
# curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# apt update --allow-insecure-repositories

# ACCEPT_EULA=Y apt install -y --allow-unauthenticated msodbcsql17
# ACCEPT_EULA=Y apt install -y --allow-unauthenticated mssql-tools

# apt update --allow-insecure-repositories && apt upgrade -y

apt autoremove
apt autoclean


