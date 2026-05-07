# Lab 14.1 - PostgreSQL Demo

This folder contains a practical implementation for the PostgreSQL part of lab 14.

Files:
- `schema.sql` - real PostgreSQL schema and seed data
- `queries.sql` - analytical SQL queries and index example
- `docker-compose.yml` - local PostgreSQL service for manual work in `psql`
- `run_demo.py` - local smoke demo that replays the same logic on SQLite

Quick start:

```bash
python run_demo.py
```

If you want the real PostgreSQL flow:

```bash
docker compose up -d
docker exec -i lab14-postgres psql -U postgres -d lab14_shop < schema.sql
docker exec -i lab14-postgres psql -U postgres -d lab14_shop < queries.sql
```
