#!/usr/bin/env bash
#Exit immediately if a command fails
set -o errexit  

#install all python dependencies
pip install -r requirements.txt

#collect static files(CSS, JavaScript, Images) for production
python manage.py collectstatic --no-input

#Run database migrations
python manage.py migrate