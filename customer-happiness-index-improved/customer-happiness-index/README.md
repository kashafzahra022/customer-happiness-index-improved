# Customer Pulse

A Flask-based financial customer happiness POC. Vercel runs the Flask app, and Supabase Postgres stores accounts and reviews persistently.

## Run locally (Windows)

Use Python 3.10 or newer. From PowerShell in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000`. Without `DATABASE_URL`, local development uses SQLite at `instance/customer_happiness.sqlite3`. The 46 sample reviews load automatically when the database is empty. Local demo login: `admin` / `admin123`.

Run tests with `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.

## Features

- Create account, sign in, and administrator-only sample reload/delete controls.
- Dashboard with CHI, total reviews, positive/neutral/negative counts, doughnut, category bar, and 7-day trend charts.
- Review table with text search and sentiment/category/source/date filters.
- Single-review analysis and CSV bulk import. Choose `Website` as the source for website feedback entered manually. CSV requires a `review`, `text`, `feedback`, or `comment` column; optional columns are `source`/`channel` and `date`/`review_date`.
- Analyst-created reviews are account-scoped. Sample reviews are shared; administrators retain a global view. Emails, Singapore NRIC/FIN patterns, and long number sequences are redacted before analysis/storage, including during migration of existing records.
- Insights with top positive/negative categories, category-wise CHI, and CSV exports.
- 46 illustrative banking reviews in `sample_reviews.csv`.

VADER's compound score ranges from −1 to +1. Labels use positive `>= 0.05`, neutral between thresholds, and negative `<= -0.05`. CHI assigns positive reviews 100 points, neutral 50, and negative 0: `(positive + 0.5 * neutral) / total * 100`.

## Deploy to Vercel

1. Create a Supabase project and open **Connect**. Copy the **Transaction Pooler** connection string (serverless mode, usually port `6543`). Keep its password private.
2. Push the complete repository to GitHub, including `app.py`, `database.py`, `requirements.txt`, `templates/`, `public/static/`, `sample_reviews.csv`, and `vercel.json`.
3. In Vercel, import the GitHub repository.
4. In Vercel Project Settings → Environment Variables, add `DATABASE_URL`, `SECRET_KEY`, and `ADMIN_PASSWORD`. Also set `ADMIN_USERNAME=admin` and `SHOW_DEMO_CREDENTIALS=false`. Use a strong random secret/password and enable them for Production (and Preview if needed).
5. Redeploy. Vercel detects the Flask `app` in root `app.py`; `vercel.json` includes the templates and sample CSV. The app creates the Postgres tables and seeds sample reviews when the review table is empty.

Vercel's filesystem is not the persistent database. Supabase stores reviews/accounts across deployments; use its Transaction Pooler URL with SSL. Never commit `.env` or database credentials. `.env.example` contains placeholders only.

## Demo mode (no setup)

If `DATABASE_URL` is not set on Vercel, the app runs in demo mode: it uses a temporary SQLite file in `/tmp`, loads the 46 sample reviews, and you sign in by creating an account at `/register`. Data is temporary and can reset on redeploy or cold start; admin login is disabled until `ADMIN_PASSWORD` is set. For permanent storage set `DATABASE_URL`, `SECRET_KEY` and `ADMIN_PASSWORD`. Check `/health` for status.

## POC limitations

VADER is intended for English and may misread Urdu, Roman Urdu, sarcasm, or financial context. Categories use keyword rules for App, Loans, Fees, Cards, Payments, Branch, Service, and Accounts; unmatched reviews become General. PII redaction is pattern-based and cannot guarantee detection of names, addresses, or every identifier. Analysts are isolated from one another, but administrators can view all reviews; this is not banking-grade security or compliance certification. Use synthetic/anonymized data, not real customer financial information.

## Sentiment accuracy and evaluation

VADER is extended with a banking lexicon (`BANKING_LEXICON` in `app.py`) for complaints and praise that general VADER scores as neutral, such as "on hold", "pending", "blocked", "nobody solved", "smooth", and "sorted out". Multi-word phrases are joined before scoring so VADER can match them.

Measured accuracy against hand labels (run `python evaluation/evaluate.py`):

| Set | Plain VADER | With banking lexicon |
|---|---|---|
| Fresh held-out set, 30 reviews, written and labeled before testing | 53% | 63% |
| Bundled sample, 46 reviews | 59% | 83% (used while developing, so optimistic) |

The 30-review fresh set has now been viewed during development, so future changes need a new held-out set. The 31-review set in `evaluation/holdout.py` is contaminated and must not be used as a clean test. All labels are one person's judgement, so treat these numbers as indicative, not validated.

Explicit negated-resolution phrases such as "nobody solved the problem" have a targeted rule and regression test. Complex negation and sarcasm can still be misclassified.
