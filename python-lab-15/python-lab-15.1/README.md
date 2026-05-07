# Lab 15.1 - ETL Pipeline

Local ETL pipeline for sales analytics.

What it does:
- loads raw CSV data
- removes duplicates
- fills missing values
- filters anomalies
- computes revenue fields
- writes cleaned and aggregated data to SQLite
- saves charts into `reports/`

Run:

```bash
pip install -r requirements.txt
python run_etl.py
```
