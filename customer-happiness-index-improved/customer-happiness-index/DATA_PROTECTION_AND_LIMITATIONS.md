# Data protection and limitations

## Data handling (POC)
- Use synthetic or fully anonymized reviews only. Do not load real customer names, account numbers, NRIC/FIN, phone numbers, or card details.
- Manual and CSV review text is scrubbed before analysis and storage for email addresses, Singapore NRIC/FIN patterns, and long number sequences commonly used for cards, accounts, or phone numbers. Existing SQLite/Postgres review text receives the same scrub during startup migration.
- Pattern matching is not a guarantee: names, addresses, unusual identifiers, and obfuscated values may remain; ordinary long numbers may also be masked. Continue to anonymize data before upload.
- Analyst-created reviews are isolated by account. Seeded sample reviews are shared, and administrators can access all reviews. Legacy non-sample reviews are assigned to administrator ownership during migration.
- This POC does not implement SSO/MFA, per-token rate limits, immutable audit logs, configurable retention/deletion workflows, or a formal security assessment. It is not banking-grade authentication or compliance certification.

## Regulatory considerations (require independent production review)
- Singapore Personal Data Protection Act (PDPA): purpose limitation, consent or legitimate basis for using customer feedback, retention limits, and access/correction requests.
- MAS technology risk management and outsourcing guidelines, if a bank deploys this with a third-party sentiment service.
- Data residency: check where the Supabase/Vercel region stores data before using real customer feedback.

## Accuracy and validity
- Sentiment labels come from VADER with a banking lexicon. Measured accuracy on a fresh 30-review set is 63% (53% without the lexicon). This is below what production use would need.
- CHI is a proposed index. It has not been validated against CSAT or NPS.
- Categories use keyword rules and have not been measured for accuracy.

## Language coverage
- VADER is designed for English. Singlish, Malay, Mandarin, and Tamil reviews are not handled reliably.

## Next steps before production
1. Complete a privacy and threat-model review, and implement approved retention, deletion, access-review, and audit requirements.
2. Add organization-approved SSO/MFA, rate limits, operational monitoring, and security testing.
3. If automatic source-system ingestion is needed later, design and security-review the required integrations before enabling them.
4. Label 150-200 representative reviews with two annotators, compare models, and validate CHI against CSAT/NPS.
5. Add and evaluate multilingual handling before claiming support for more languages.
