#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements/requirements.txt

python domiciles/manage.py collectstatic --no-input
python domiciles/manage.py migrate
python domiciles/manage.py runserver