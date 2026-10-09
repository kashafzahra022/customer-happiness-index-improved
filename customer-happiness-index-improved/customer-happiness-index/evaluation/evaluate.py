# Run from project root: python evaluation/evaluate.py
import csv, sys
from pathlib import Path; ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'evaluation'))
from app import analyze_review, calculate_chi
from holdout import HOLDOUT
GOLD_PHRASES = {
 'quick and easy to use':'positive','approved quickly':'positive','service fee was clearly':'positive','resolved my card issue':'positive',
 'keeps crashing':'negative','waited two weeks':'negative','international transfer charge':'negative','Branch staff were friendly':'positive',
 'debit card arrived':'positive','unexpected monthly account fee':'negative','mortgage advisor answered':'positive','login screen is confusing':'negative',
 'bill payment went through':'positive','called three times':'negative','long queue':'negative','savings account interest rate':'positive',
 'cannot download my monthly statement':'negative','support representative was patient':'positive','card was blocked':'negative',
 'loan repayment schedule':'positive','charged twice':'negative','ATM near my office':'positive','app is fine':'positive','overdraft fee feels unfair':'negative',
 'Opening a business account':'positive','loan documents were lost':'negative','contactless card works':'positive','on hold for 40 minutes':'negative',
 'online banking website is easy':'positive','transfer is still pending':'negative','staff explained the account options':'positive',
 'too many steps':'negative','personal loan rate was fair':'positive','account was locked':'negative','app notifications help':'positive',
 'cash withdrawal failed':'negative','branch is clean':'positive','annual card fee is too high':'negative','mortgage payment posted':'positive',
 'clear updates throughout the car loan':'positive','replacement card came in two days':'positive','account dashboard shows':'positive',
 'applied to the wrong account':'negative','Customer care transferred':'negative','mobile deposit feature':'positive','service at my local branch':'positive'}
rows = list(csv.DictReader(open(str(ROOT / 'sample_reviews.csv'), encoding='utf-8-sig')))
sample = []
for r in rows:
    hits = [v for k, v in GOLD_PHRASES.items() if k.lower() in r['review'].lower()]
    assert len(hits) == 1, r['review']
    sample.append((r['review'], hits[0]))
def acc(pairs):
    ok = sum(analyze_review(t)['sentiment'] == g for t, g in pairs)
    return ok, len(pairs), round(ok / len(pairs) * 100, 1)
def chi_gap(pairs):
    tool = calculate_chi([{'sentiment': analyze_review(t)['sentiment']} for t, _ in pairs])
    gold = calculate_chi([{'sentiment': g} for _, g in pairs])
    return tool, gold
print('sample (46, tuned-on, for reference):', acc(sample), 'CHI tool vs gold:', chi_gap(sample))
print('holdout (31, unseen):', acc(HOLDOUT), 'CHI tool vs gold:', chi_gap(HOLDOUT))
from holdout2 import HOLDOUT2
from collections import Counter
print('holdout2 label mix:', Counter(l for _, l in HOLDOUT2))
print('holdout2 (30, fresh, run once):', acc(HOLDOUT2), 'CHI tool vs gold:', chi_gap(HOLDOUT2))
for t, g in HOLDOUT2:
    p = analyze_review(t)['sentiment']
    if p != g: print(f'  gold={g[:3]} pred={p[:3]} | {t}')
