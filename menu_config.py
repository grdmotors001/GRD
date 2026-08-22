# -----------------------------------------------------------------------------
# menu_config.py
#
# This file is the single source of truth for the eBill web app's navigation.
# It mirrors the ORIGINAL desktop software's menu structure exactly:
#   Setup | Vouchers | Stock | Reports | Utilities | Exit
#
# Each entry has:
#   key       -> unique slug used in the URL (/m/<key>)
#   label     -> exact label as seen in the original software
#   kind      -> "master"   -> full CRUD screen (built already, or generic)
#                "placeholder" -> page exists, navigable, marked "coming soon"
#   fields    -> for masters, the form fields to show (label, name, type)
# -----------------------------------------------------------------------------

MENU = {
    "Setup": [
        {"key": "dealer",            "label": "1. Dealer Master",                        "kind": "custom"},
        {"key": "party",             "label": "2. Party Master List (Raw Material Purchase Parties)", "kind": "simple",
         "fields": [("name", "Name", "text"), ("address", "Address", "text"), ("mobile", "Mobile No.", "text"), ("extra", "GSTIN", "text")]},
        {"key": "product",           "label": "3. Product Master",                       "kind": "custom"},
        {"key": "battery-maker",     "label": "4. Battery Maker Master",                 "kind": "simple",
         "fields": [("name", "Battery Maker Name", "text")]},
        {"key": "rto",               "label": "5. RTO Master",                           "kind": "simple",
         "fields": [("name", "RTO Name", "text"), ("code", "RTO Code", "text"), ("address", "Address (4 line)", "textarea")]},
        {"key": "financer",          "label": "6. Financer Master",                      "kind": "simple",
         "fields": [("name", "Name", "text"), ("address", "Address", "text")]},
        {"key": "production-formula","label": "7. Production Formula",                   "kind": "custom"},
        {"key": "mechanic",          "label": "8. Machnic Master",                       "kind": "simple",
         "fields": [("name", "Mechanic Name", "text")]},
        {"key": "user",              "label": "9. User Master",                          "kind": "custom"},
        {"key": "option-setting",    "label": "A. User wise Option Setting",             "kind": "custom"},
        {"key": "bank",              "label": "B. Bank Details",                         "kind": "simple",
         "fields": [("name", "Bank Name", "text"), ("account_no", "Account No.", "text"), ("ifsc", "IFSC", "text"),
                    ("is_default", "Default / Primary (auto-fills on new Invoices)", "checkbox")]},
        {"key": "colour",            "label": "=. Colour Master",                        "kind": "simple",
         "fields": [("name", "Colour", "text"), ("code", "Colour Code", "text")]},
    ],
    "Vouchers": [
        {"key": "purchase-bills",         "label": "C. Purchase Bills",                  "kind": "custom"},
        {"key": "production-voucher",     "label": "D. Production Voucher",              "kind": "custom"},
        {"key": "delivery-challan",       "label": "E. E-Rickshaw Delivery Challan",     "kind": "custom"},
        {"key": "tax-invoice",            "label": "F. Tax Invoice",                     "kind": "custom"},
        {"key": "old-rickshaw",           "label": "G. Old Rickshaw",                    "kind": "custom"},
        {"key": "battery-delivery-challan","label": "H. Battery Delivery Challan",       "kind": "custom"},
        {"key": "journal-stock",          "label": "I. Journal Stock",                   "kind": "custom"},
    ],
    "Stock": [
        {"key": "closing-stock-premises",   "label": "J. Closing Stock - E-Rickshaw at Premises", "kind": "custom"},
        {"key": "closing-stock-dealers",    "label": "K. Closing Stock - E-Rickshaw with Dealers", "kind": "custom"},
        {"key": "closing-stock-raw",        "label": "L. Closing Stock - Raw Material",           "kind": "custom"},
        {"key": "stock-ledger-premises",    "label": "M. Stock Ledger - Premises",                "kind": "custom"},
        {"key": "stock-ledger-dealers",     "label": "N. Stock Ledger - E-Rickshaw with Dealers",  "kind": "custom"},
    ],
    "Reports": [
        {"key": "purchase-register",         "label": "O. Purchase Register",           "kind": "custom"},
        {"key": "production-register",       "label": "P. Production Register",         "kind": "custom"},
        {"key": "delivery-challan-register", "label": "Q. Delivery Challan Register",   "kind": "custom"},
        {"key": "sale-register",             "label": "R. Sale Register",               "kind": "custom"},
        {"key": "gst-register",              "label": "S. GST Register",                "kind": "custom"},
        {"key": "hypothecation-register",    "label": "T. Hypothecation Register",      "kind": "custom"},
        {"key": "payment-receivable-report", "label": "U. Payment Rec'able Report",     "kind": "custom"},
        {"key": "subsidy-report",            "label": "V. Subsidy Report",              "kind": "custom"},
        {"key": "ledger",                    "label": "W. Ledger",                      "kind": "custom"},
        {"key": "password",                  "label": "X. Password",                    "kind": "custom"},
    ],
    "Utilities": [
        {"key": "backup-restore",  "label": "Backup / Restore",       "kind": "placeholder"},
        {"key": "import-data",     "label": "Import Old Data (Excel / MDB)", "kind": "custom"},
    ],
}

def all_items():
    """Flat list of every menu item, with its category attached."""
    out = []
    for category, items in MENU.items():
        for item in items:
            out.append({**item, "category": category})
    return out


def find_item(key):
    for item in all_items():
        if item["key"] == key:
            return item
    return None
