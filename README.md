# Maison Moche

E-commerce platform built from scratch. Django REST API backend, PostgreSQL database, React frontend (in progress).

Built as a portfolio project — the goal is to build and understand every layer of the stack.

## Stack

- **Backend** — Django + Django REST Framework
- **Database** — PostgreSQL
- **Auth** — JWT via djangorestframework-simplejwt
- **Payments** — Mollie (iDEAL)
- **Frontend** — React

## Status

- [x] Data models — products, variants, categories, suppliers, brands, collections
- [x] Custom user model + JWT auth setup
- [ ] Product catalog API
- [ ] Cart & checkout
- [ ] Supplier feed ingestion (CSV)
- [ ] Frontend

## Run locally

```bash
git clone https://github.com/RodneyRingworm/Maison-Moche
cd Maison-Moche
pip install -r requirements.txt
# add .env with DB credentials
python manage.py migrate
python manage.py runserver
```
