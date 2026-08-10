# AWS EC2 deployment — VoteSecure

## 1. Prepare EC2

Use an Ubuntu LTS EC2 instance eligible under your AWS Free Tier/credits.

Security group:

- TCP 22: your public IP only
- TCP 80: `0.0.0.0/0`
- TCP 443: `0.0.0.0/0`
- Do not expose PostgreSQL 5432 publicly.

## 2. Install packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git
```

Clone:

```bash
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/votesecure.git
sudo chown -R $USER:$USER /var/www/votesecure
cd /var/www/votesecure
```

## 3. Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment

```bash
cp .env.example .env
nano .env
```

Production minimum:

```env
DEBUG=False
SECRET_KEY=generate-a-long-random-secret
ALLOWED_HOSTS=YOUR_EC2_PUBLIC_DNS,YOUR_DOMAIN
```

If using RDS, also configure the DB variables shown in the main README.

## 5. Database and static files

```bash
python manage.py migrate
python manage.py seed_candidates
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py check --deploy
```

## 6. Test Gunicorn

```bash
source .venv/bin/activate
gunicorn mysite.wsgi:application --bind 127.0.0.1:8000
```

In another SSH session:

```bash
curl http://127.0.0.1:8000/health/
```

## 7. Create systemd service

Create `/etc/systemd/system/votesecure.service`:

```ini
[Unit]
Description=VoteSecure Django application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/votesecure
EnvironmentFile=/var/www/votesecure/.env
ExecStart=/var/www/votesecure/.venv/bin/gunicorn mysite.wsgi:application --bind 127.0.0.1:8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable votesecure
sudo systemctl start votesecure
sudo systemctl status votesecure
```

## 8. Nginx

Create `/etc/nginx/sites-available/votesecure`:

```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_DNS;

    location /static/ {
        alias /var/www/votesecure/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/votesecure /etc/nginx/sites-enabled/votesecure
sudo nginx -t
sudo systemctl restart nginx
```

## 9. HTTPS

For a real public deployment, use a domain name and Let's Encrypt/Certbot. Do not treat plain HTTP as a production security configuration.

## 10. Updating after a GitHub push

```bash
cd /var/www/votesecure
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart votesecure
```
