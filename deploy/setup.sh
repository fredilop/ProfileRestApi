#!/usr/bin/env bash

set -e
echo "ALFLAG -> Constant variables..."
# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/fredilop/ProfileRestApi.git'

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'
echo "ALFLAG -> Constant variables... DONE"


# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
echo "ALFLAG -> Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git
echo "ALFLAG -> Installing dependencies... DONE"

echo "ALFLAG -> Clonning project..."
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/profiles-rest-api
echo "ALFLAG -> Clonning project..."

echo "ALFLAG -> Virtual env..."
mkdir -p $VIRTUALENV_BASE_PATH
python3 -m venv $VIRTUALENV_BASE_PATH/profiles_api
echo "ALFLAG -> Virtual env... DONE"

echo "ALFLAG -> Installing requirements txt..."
# $VIRTUALENV_BASE_PATH/profiles_api/bin/pip install -r $PROJECT_BASE_PATH/profiles-rest-api/requirements.txt
$VIRTUALENV_BASE_PATH/profiles_api/bin/pip install Django
$VIRTUALENV_BASE_PATH/profiles_api/bin/pip install djangorestframework
echo "ALFLAG -> Installing requirements txt... DONE"

# Run migrations
echo "ALFLAG -> Run migrations and collecstatic..."
# cd $PROJECT_BASE_PATH/profiles-rest-api/src

# Run migrations and collectstatic
# cd $PROJECT_BASE_PATH
# $PROJECT_BASE_PATH/env/bin/python manage.py migrate
# $PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
echo "ALFLAG -> Run migrations... DONE"


echo "ALFLAG -> Supervisor setup..."
# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/profiles-rest-api/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart profiles_api
echo "ALFLAG -> Supervisor setup... DONE"

echo "ALFLAG -> Nginx..."
# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/profiles-rest-api/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf
systemctl restart nginx.service
echo "ALFLAG -> Nginx... DONE"

echo "DONE! :)"
