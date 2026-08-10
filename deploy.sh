#!/usr/bin/env bash
set -e
source .venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_candidates
python manage.py collectstatic --noinput
python manage.py check --deploy
sudo systemctl restart votesecure
