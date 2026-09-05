# Online Feedback Collector with Admin Dashboard

A professional full-stack feedback collection system built with **Python, Flask, SQLite, HTML, CSS, JavaScript, Bootstrap, Jinja2 and Chart.js**.

## Features

- Responsive feedback form
- Name, email, rating and comments
- Server-side validation
- SQLite database storage
- Admin login
- Admin dashboard
- Total feedback and average rating
- Rating distribution chart
- Feedback table
- CSV export
- JSON REST endpoint: `/api/feedback`

## Project Structure

```text
OnlineFeedbackCollector/
├── app.py
├── requirements.txt
├── database.db
├── README.md
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── admin_login.html
│   └── admin.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Run Locally

```bash
python -m venv venv
```

Windows:
```bash
venv\\Scripts\\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the application:
```bash
python app.py
```

Open:
`http://127.0.0.1:5000`

## Admin

Demo login:
- Username: `admin`
- Password: `admin123`

**Change the demo credentials and Flask secret key before production deployment.**

## Main Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Feedback form |
| `/submit-feedback` | POST | Store feedback |
| `/admin-login` | GET/POST | Admin authentication |
| `/admin-dashboard` | GET | Dashboard |
| `/export-csv` | GET | Download CSV |
| `/api/feedback` | GET | JSON feedback API |

## GitHub

```bash
git init
git add .
git commit -m "Initial commit - Online Feedback Collector"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Production Notes

- Use environment variables for secrets and admin credentials.
- Disable Flask debug mode in production.
- Add CSRF protection for production.
- Use a production WSGI server.
- Consider PostgreSQL for larger deployments.
