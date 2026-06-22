# Maison Moche

> *"Objects of questionable necessity, presented with absolute conviction."*

Maison Moche is a full-stack e-commerce platform built from scratch as a portfolio project. The store's fictional brand sells cursed French home goods with the seriousness of a museum retrospective. The codebase solves the real problems that platforms like Shopify abstract away — inventory reservation, supplier feed ingestion, JWT auth, and a decoupled REST + React architecture.

**Status:** Phase 1 complete (environment + Django/PostgreSQL connected). Phase 2 in progress (data models).

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Django + Django REST Framework |
| Database | PostgreSQL |
| Auth | JWT (djangorestframework-simplejwt) |
| Frontend | React (Vite) — Phase 8 |
| Payments | Stripe (sandbox) — Phase 5 |

---

## Why These Choices

Every architectural decision was reasoned through before writing code. The short version:

**Django over Flask/FastAPI** — Flask gives you nothing out of the box; every decision (ORM, auth, migrations) has to be made separately. Django comes with all of that built in, which means less configuration and more time on actual features. DRF adds serializers and class-based views on top, which makes building REST APIs significantly faster without sacrificing control.

**PostgreSQL over SQLite** — SQLite is fine for toy projects but doesn't support concurrent writes, enforced constraints, or production-grade features. This project has stock reservation logic that requires row-level locking. PostgreSQL handles that properly.

**Decoupled REST + React over monolith** — Keeping the backend as a pure API and the frontend as a separate React app means they can be developed, deployed, and scaled independently. The API is also testable with Postman before the frontend exists.

**JWT over session auth** — Sessions require server-side state. JWT tokens are self-contained — the backend can verify them without a database lookup. Better fit for a decoupled frontend that makes API calls from the browser.

---

## Project Structure

```
maison-moche/
├── backend/
│   ├── ecommerce/          ← Django project config (settings, urls, wsgi)
│   ├── users/              ← Custom user model, register/login endpoints
│   ├── products/           ← Product, Category, Image models + API
│   ├── orders/             ← Cart, Order, OrderItem models + checkout
│   ├── inventory/          ← Stock levels, reservation logic, low-stock alerts
│   ├── feeds/              ← CSV upload, feed parser, import logs
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── pages/          ← One component per page
│   │   ├── components/     ← Reusable UI elements
│   │   └── api/            ← Functions that call the backend
│   └── package.json
├── .env                    ← Secret keys + DB credentials (not committed)
├── .gitignore
└── README.md
```

---

## Data Model

Core tables and their relationships:

```
users
  └── addresses (FK → users)
  └── orders    (FK → users)
        └── order_items (FK → orders, FK → products)

categories
  └── products (FK → categories)
        └── product_images   (FK → products)
        └── inventory_levels (one-to-one with products)

supplier_feeds
  └── feed_items (FK → supplier_feeds)
```

**Key design decisions:**

- `unit_price` is snapshotted on `order_items` at purchase time — if a product price changes later, historical order totals stay accurate.
- Stock availability is `quantity_on_hand − quantity_reserved`. Reservation happens when an item is added to cart, preventing two customers from buying the last unit simultaneously.
- `is_active` on products enables soft deletion — products are hidden from the storefront without losing order history that references them.

---

## API Endpoints

All endpoints prefixed with `/api/`. Authenticated routes require a JWT token in the `Authorization` header.

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create account, returns JWT |
| POST | `/api/auth/login` | Login, returns JWT |
| POST | `/api/auth/logout` | Invalidate token |
| GET | `/api/auth/me` | Current user profile |

### Products
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | List active products. Supports `?category=`, `?search=`, `?page=` |
| GET | `/api/products/{id}/` | Product detail with images and stock status |
| GET | `/api/categories/` | List all categories |
| POST | `/api/admin/products/` | Create product (admin only) |
| PATCH | `/api/admin/products/{id}/` | Update product (admin only) |
| DELETE | `/api/admin/products/{id}/` | Soft delete — sets `is_active=false` (admin only) |

### Cart & Orders
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/cart/` | View cart contents and total |
| POST | `/api/cart/` | Add item. Body: `{product_id, quantity}` |
| PATCH | `/api/cart/{item_id}/` | Update quantity |
| DELETE | `/api/cart/{item_id}/` | Remove item |
| POST | `/api/orders/` | Create order from cart + Stripe payment |
| GET | `/api/orders/` | Order history (auth required) |
| GET | `/api/orders/{id}/` | Order detail |

### Inventory & Feeds (admin)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/inventory/` | All products with current stock levels |
| PATCH | `/api/admin/inventory/{id}/` | Manual stock adjustment |
| GET | `/api/admin/inventory/low-stock/` | Products below reorder point |
| POST | `/api/admin/feeds/upload/` | Upload supplier CSV |
| GET | `/api/admin/feeds/` | Feed upload history |
| GET | `/api/admin/feeds/{id}/items/` | Row-level results for a specific upload |

---

## Supplier CSV Feed

Suppliers send stock and product data as CSV. The backend validates, parses, and upserts.

**Required columns:** `sku`, `name`, `price`, `quantity`

**Optional columns:** `category`, `description`, `image_url`

**Processing logic:**
- If SKU exists → update price and stock level
- If SKU is new → create product and inventory record
- If category doesn't exist → create it automatically
- Every row is logged to `feed_items` with a `synced` or `failed` status and an error message if applicable

---

## Build Phases

| Phase | Description | Status |
|---|---|---|
| 1 | Environment setup, Django + PostgreSQL connected | ✅ Done |
| 2 | Data models and migrations | 🔄 In progress |
| 3 | JWT auth, custom user model | ⬜ Planned |
| 4 | Product catalog API | ⬜ Planned |
| 5 | Cart, checkout, Stripe integration | ⬜ Planned |
| 6 | Inventory system and stock reservation | ⬜ Planned |
| 7 | Supplier CSV feed ingestion | ⬜ Planned |
| 8 | React frontend | ⬜ Planned |
| 9 | Deploy (Railway + Vercel) | ⬜ Planned |

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/maison-moche.git
cd maison-moche/backend

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary stripe python-decouple

# Create .env file (see .env.example)
# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

**.env.example:**
```
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/maison_moche
DEBUG=True
```

---

## Background

This project exists because e-commerce operations work — configuring Shopify, ChannelEngine, ContentServ, managing supplier feeds, onboarding vendors — gave me a deep understanding of how these systems work from the outside. This is the exercise of building one from the inside: implementing the things those platforms abstract away, and understanding why they work the way they do.
