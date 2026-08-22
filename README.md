# eBill — Web Edition (skeleton)

A web version of the original **eBill (1.0) - G.R.D. MOTORS** desktop software
(E-Rickshaw manufacturing / dealer billing / inventory / accounts).

This is the **full navigation skeleton**: every menu item from the original
software (Setup, Vouchers, Stock, Reports, Utilities) is wired up and clickable.
Three modules are fully built as a working reference (Dealer Master, Product
Master, User Master); the rest show a "coming soon" page until we build them
one by one, so nothing is a dead link.

## What's included

- Same menu structure: **Setup | Vouchers | Stock | Reports | Utilities**
- Dashboard homepage with the launcher grid (all modules) + the chassis
  pipeline table (Manufacturing → Delivery Challan → Tax Invoice), same as
  the original "Dashboard as on `<date>`" screen.
- Dealer Master, Product Master, User Master — full add/edit/delete.
- **Production Voucher** — records a finished vehicle coming off the line;
  auto-copies the Bill of Material (if imported) as consumed raw-material
  lines, and creates the chassis in the Dashboard's "Manufacturing" section.
- **Delivery Challan** — dispatches an already-manufactured chassis to a
  dealer; picking the chassis auto-fills its motor/controller/colour, and
  saving moves it to the Dashboard's "Delivery Challan" section. Includes
  Cancel (returns chassis to Manufacturing) and Delete. Print view uses the
  branded "Delivery Challan / Warranty Card" design (dealer + brand strip,
  vehicle particulars, battery, accessories YES/NO, declaration, signatures).
  Shows the specific model's logo if one is placed in `static/logos/` (named
  after the product's UMRN Code or Item Code — see `static/logos/README.txt`);
  falls back to the generic multi-brand strip if no matching file is found.
- Colour, Battery Maker, RTO, Financer, Mechanic, Bank, Party — simple
  add/edit/delete masters (generic screen, same pattern for all of them).
- **Tax Invoice** — the GST sale invoice, raised against a Delivery Challan.
  Automatically splits CGST+SGST (in-state) vs IGST (out-of-state) based on
  the buyer's state code, same logic as the original. Includes a print-ready
  invoice view styled after the original `billto.frx` layout (buyer details,
  chassis/motor/colour, GST breakdown, bill total) — use your browser's
  Print → Save as PDF.
- **Purchase Bills** — raw-material purchases from a party, with multiple
  item lines per bill (Item Name, HSN, Qty, Rate, GST%). Auto-fills HSN/GST%
  from Product Master when you pick a known raw material. Same CGST+SGST vs
  IGST split logic as Tax Invoice, based on the party's state code.
- **Old Rickshaw** — buy-back/trade-in of a used e-rickshaw, tracked by
  vehicle registration number (not chassis) since it's independent of the
  manufacturing pipeline. Tracks sold amount, receipt amount, running
  balance, and optional resale details.
- **Battery Delivery Challan** — a battery sent to a dealer on its own (e.g.
  a warranty replacement), separate from a full vehicle Delivery Challan.
- **Journal Stock** — manual stock correction (raw material or finished
  item) for anything that doesn't come from a Purchase Bill, Production
  Voucher, or Delivery Challan — e.g. fixing a stock-take discrepancy.
  Raw-material entries automatically feed into Closing Stock - Raw Material.
- **Import Old Data** page (Utilities menu): upload an Excel export in the
  same layout as `Book1.xlsx` and it loads Dealers, Products, Colours,
  Battery Makers, Financers, Mechanics, Production Formula (BOM), the
  Chassis/Vehicle register, and Users straight into the new database.
- **Stock screens** — all 5, computed live from the vouchers above (no
  separate data entry needed):
  - *Closing Stock at Premises* — vehicles manufactured but not yet sent out
  - *Closing Stock with Dealers* — delivered but not yet invoiced/sold
  - *Closing Stock - Raw Material* — purchased minus consumed, per item
  - *Stock Ledger - Premises* — chronological IN (Production) / OUT
    (Delivery Challan) with running balance, filterable by date range
  - *Stock Ledger - with Dealers* — chronological IN (Delivery Challan) /
    OUT (Tax Invoice) per dealer, with running balance, filterable by
    dealer and date range
- **All 10 Reports/Utilities** — all computed live, no separate entry:
  - *Purchase Register* — every raw-material line purchased, with GST split
  - *Production Register* — every vehicle manufactured
  - *Delivery Challan Register* — every dispatch to a dealer
  - *Sale Register* — every Tax Invoice, same columns as the original
  - *GST Register* — Outward (sales) vs Inward (purchases) GST, with net
    payable/credit
  - *Hypothecation Register* — invoices financed against a loan
  - *Payment Rec'able Report* — outstanding balance per invoice, with an
    inline "Save" to record payments as they come in
  - *Subsidy Report* — invoices with a government subsidy applied
  - *Ledger* — per-dealer account statement (Tax Invoice = debit, payment
    received = credit), running balance
  - *Password* — reset any user's login password (hashed, not plain text)

## Everything is now built

All modules from the original menu are complete, including the four items
that were previously "next steps":

1. **Tax Invoice branded print** — matches the Delivery Challan / Warranty
   Card treatment (italic gradient logo, vehicle brand strip, navy info-boxes
   for Invoice No. / Date / Place of Supply), on top of the GST breakup table.
2. **Production Formula (BOM) management screen** (Setup > 7) — full add/
   edit/delete, grouped by product, in addition to bulk loading via Import
   Old Data.
3. **User wise Option Setting** (Setup > A) — per-user checkbox grid of
   which menu items they can access. Super users are always unrestricted.
   Note: there's no login/session system yet, so this stores the permission
   data correctly but isn't enforced anywhere yet.
4. **Direct Access `.mdb`/`.accdb` import** (Utilities > Import Old Data) —
   upload the original Access file directly, no need to export to Excel
   first. Two backends are tried automatically:
   - **Windows** (most common case): `pip install pyodbc`, plus the free
     ["Microsoft Access Database Engine Redistributable"](https://www.microsoft.com/en-us/download/details.aspx?id=54920)
     — install the 32-bit build if your Python is 32-bit, 64-bit if it's
     64-bit (mismatched bitness is the most common failure).
   - **Linux/Mac/WSL**: the `mdbtools` command-line tools
     (`apt-get install mdbtools` or `brew install mdbtools`).

   If neither is available you'll get a clear on-screen error explaining
   both options, or you can just export the Access tables to Excel (same
   sheet/column names) and upload that instead — that path always works.

## Running it

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

First run creates `ebill.db` (SQLite) automatically, with a default login:
- username: `admin`
- password: `admin1`

(Change this from User Master once you're in — unlike the original software,
passwords are stored securely hashed, not in plain text.)

**Updating to a newer version of this app:** every time you start the app,
it automatically checks your existing `ebill.db` for any new columns added
since your last update, and adds them (safely, without touching your
existing data). You never need to delete `ebill.db` to pick up updates —
just drop in the new files and run `python app.py` as normal. (This
auto-update only applies to SQLite — see below for Postgres/MySQL.)

### Using PostgreSQL or MySQL instead of SQLite

By default the app uses a local SQLite file (`ebill.db`) — zero setup, good
for testing. For real production use with multiple people logging in at
once, point it at PostgreSQL or MySQL instead by setting the `DATABASE_URL`
environment variable before running `python app.py`:

```bash
# PostgreSQL (create the empty database first, e.g. `createdb ebill`)
export DATABASE_URL="postgresql+psycopg2://ebill_user:mypassword@localhost:5432/ebill"

# MySQL (create the empty database first, e.g. `CREATE DATABASE ebill;`)
export DATABASE_URL="mysql+pymysql://ebill_user:mypassword@localhost:3306/ebill"

python app.py
```

If `DATABASE_URL` isn't set, it falls back to the local SQLite file
automatically. `psycopg2-binary` (Postgres) and `PyMySQL` (MySQL) are both
already in `requirements.txt`, so `pip install -r requirements.txt` gets you
ready for either.

**Note:** the automatic column-adding described above only runs against
SQLite. Once you're on Postgres/MySQL for production, schema changes (when a
future update adds a new field) should go through a proper migration tool
(e.g. Alembic / Flask-Migrate) instead of an automatic ALTER TABLE — safer
for real production data. Ask and this can be set up when you're ready to
move off SQLite.

## Importing your old data

1. Open the app → **Utilities → Import Old Data (Excel / MDB)**
2. Upload your Excel export (same sheet/column names as `Book1.xlsx`)
3. It will report how many Dealers / Products / Vehicles / Users were loaded

Direct `.mdb` (Access) import will be added once we finalize field mapping —
for now export the Access tables to Excel with the same column names.

## Project layout

```
app.py            - routes
models.py         - database tables (SQLAlchemy)
menu_config.py     - the single source of truth for the menu/navigation
import_excel.py    - legacy Excel -> new database importer
templates/         - HTML pages
static/css/        - styling (mimics the original desktop look/feel)
```

## Deploying with GitHub + Vercel + Supabase

This version is prepared for the following production setup:

`GitHub -> Vercel (Flask/Python) -> Supabase PostgreSQL`

### 1. Create the Supabase database

Create a Supabase project and copy its **PostgreSQL connection string**. For Vercel/serverless, the Supabase **Transaction Pooler** connection is recommended. It normally looks like:

```text
postgresql://postgres.PROJECT_REF:PASSWORD@aws-0-REGION.pooler.supabase.com:6543/postgres?sslmode=require
```

### 2. Put the project on GitHub

Push the contents of this folder to a GitHub repository. Do not commit `.env`, passwords, or a production database file.

### 3. Import the repository into Vercel

In Vercel, import the GitHub repository. The included `vercel.json` and `api/index.py` configure the existing Flask application as a Vercel Python function.

### 4. Add Vercel Environment Variables

Add these variables for Production (and Preview if required):

- `DATABASE_URL` = Supabase PostgreSQL connection string
- `SECRET_KEY` = long random secret
- `DEFAULT_ADMIN_PASSWORD` = temporary first-login password

The application creates its SQLAlchemy tables automatically on the first serverless instance. The default company and admin user are also created if the database is empty.

### 5. First login

Open the deployed site and log in with:

- User ID: `admin`
- Password: the value of `DEFAULT_ADMIN_PASSWORD` (defaults to `admin1` only if you did not set it)

Immediately change the password from User Master / Password utility.

### Important Vercel limitation

The deployed filesystem is not persistent. Legacy Excel uploads are therefore stored temporarily in `/tmp` during an invocation. Persistent application data belongs in Supabase PostgreSQL. Static logos and letterhead remain in the repository and are served normally.

### Local development

Without `DATABASE_URL`, the app still uses a local `ebill.db` SQLite database for development. With `DATABASE_URL` set, local development can use the same Supabase PostgreSQL database as Vercel.
