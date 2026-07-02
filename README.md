# Maison Moche

E-commerce platform built from scratch. Django REST API backend, PostgreSQL database, React frontend (in progress).

Built as a portfolio project — the goal is to improve my understanding of core IT concepts and full stack development

Maison Moche is a fictional Home & Living brand that sells dubious items with the sincerity a luxury design brand.
Their branding evokes prestige and craftsmanship, their presentation borrows from heraldic imagery and parisian aesthetics.
Their products certainly look the part, until you take a closer look that is.

## Stack

- **Backend** — Django + Django REST Framework
- **Database** — PostgreSQL
- **Auth** — JWT via djangorestframework-simplejwt
- **Payments** — Mollie (iDEAL)
- **Frontend** — React

## Status

- [x] Data models — products, variants, categories, suppliers, brands, collections
- [x] Custom user model + JWT auth setup (in progress)
- [x] Product catalog API
- [ ] Cart & checkout
- [ ] Supplier feed ingestion (CSV)
- [ ] Frontend

## Planned features
- PIM connector
- Flxpoint connector

## Run locally

```bash
git clone https://github.com/lekkerleren/Maison-Moche
cd Maison-Moche
pip install -r requirements.txt
# add .env with DB credentials
python manage.py migrate
python manage.py runserver
```
