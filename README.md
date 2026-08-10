# VoteSecure — AWS-ready Django Voting Demo

> **Important:** This is an educational/demo voting application, not a real election platform. Do not enter real Aadhaar numbers, government IDs, or other sensitive personal information.

## What was improved

- Cleaned the original Django project structure.
- Removed `db.sqlite3`, Python cache files, and the hard-coded Django secret key.
- Added environment-based production settings.
- Added CSRF protection and secure cookie/HSTS settings for production.
- Added PostgreSQL/Amazon RDS support through environment variables.
- Added WhiteNoise for production static files.
- Added dynamic candidates and a results dashboard.
- Added Django admin support for candidates and votes.
- Prevents duplicate voting using a salted SHA-256 verification hash instead of storing the entered ID in plaintext.
- Added server-side validation for voter/Aadhaar-style demo IDs.
- Added responsive UI and clear demo-only warnings.
- Added health endpoint for deployment checks.
- Added GitHub Actions CI.
- Added an EC2 deployment script and AWS deployment documentation.
- Preserved the candidate images supplied in the original project.

## AWS architecture used for the project

Recommended student/demo architecture:

`GitHub → EC2 (Django + Gunicorn + Nginx) → Amazon RDS PostgreSQL`

Optional next step:

`EC2 → S3` for backups/media, if needed.

AWS Free Tier eligibility depends on your account and current Free Tier plan. AWS currently offers new customers Free Tier credits and a Free account plan for eligible services; check the AWS console before creating paid resources.

## Local setup

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_candidates
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

Open:

- Home: http://127.0.0.1:8000/
- Vote: http://127.0.0.1:8000/vote/
- Results: http://127.0.0.1:8000/results/
- Admin: http://127.0.0.1:8000/admin/
- Health: http://127.0.0.1:8000/health/

## Git + GitHub process

```bash
git init
git add .
git commit -m "Initial AWS-ready VoteSecure application"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/votesecure.git
git push -u origin main
```

For later changes:

```bash
git status
git add .
git commit -m "Describe the change"
git push origin main
```

Do **not** commit `.env`, passwords, AWS keys, database credentials, or `db.sqlite3`.

## Deploy to AWS EC2

1. Create an Ubuntu EC2 instance that is covered by your AWS Free Tier/credits.
2. Configure a security group with:
   - SSH 22 — only from your IP
   - HTTP 80 — anywhere
   - HTTPS 443 — anywhere
3. SSH into the instance.
4. Install Python, Git, Nginx, and build dependencies.
5. Clone this GitHub repository.
6. Create a `.env` file on EC2.
7. Run migrations and collectstatic.
8. Run Gunicorn behind Nginx.

Example commands are in `docs/AWS_EC2_DEPLOYMENT.md`.

## Amazon RDS PostgreSQL

For a production-like database, create a PostgreSQL RDS instance and set:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=votesecure
DB_USER=...
DB_PASSWORD=...
DB_HOST=your-rds-endpoint
DB_PORT=5432
```

Keep RDS private where possible and allow inbound PostgreSQL traffic only from the EC2 security group.

## GitHub Actions

`.github/workflows/ci.yml` runs Django checks on pushes and pull requests.

The project deliberately does not hard-code AWS credentials. If you later want automatic EC2 deployment from GitHub Actions, add GitHub Actions secrets for an SSH deployment key and host, then build the workflow around your own infrastructure.

## Security notes

This demo hashes the submitted verification identifier before storing it. It does not make an online election system secure or legally compliant. A real election system requires much stronger identity verification, cryptographic controls, auditability, privacy controls, threat modeling, accessibility, legal compliance, independent security review, and appropriate election authority integration.
