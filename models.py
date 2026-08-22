from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Company(db.Model):
    """Single-row table: overall company / financial-year profile (old Sheet 'FLD')."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), default="G.R.D. MOTORS")
    year = db.Column(db.String(20), default="20212022")
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    state = db.Column(db.String(100))
    mobile = db.Column(db.String(30))
    email = db.Column(db.String(120))
    website = db.Column(db.String(120))
    gst_no = db.Column(db.String(30))
    bank_name = db.Column(db.String(120))
    bank_account = db.Column(db.String(50))
    bank_ifsc = db.Column(db.String(50))
    state_code = db.Column(db.String(10))


class SimpleMaster(db.Model):
    """
    Generic table used for the small 'code + name (+extra)' masters:
    Party, Battery Maker, RTO, Financer, Mechanic, Bank, Colour.
    'kind' distinguishes which master a row belongs to.
    """
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(40), index=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50))
    address = db.Column(db.String(300))
    mobile = db.Column(db.String(30))
    account_no = db.Column(db.String(50))
    is_default = db.Column(db.Boolean, default=False)  # e.g. the Bank to use on invoices when none is picked explicitly
    ifsc = db.Column(db.String(50))
    extra = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dealer(db.Model):
    """Dealer Master (Setup > 1. Dealer Master) — legacy Sheet9 'AMC' table."""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)          # AMCODE, e.g. A-01
    name = db.Column(db.String(200), nullable=False)      # AMN
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    mobile = db.Column(db.String(30))
    gst_no = db.Column(db.String(30))
    state = db.Column(db.String(100))
    state_code = db.Column(db.String(10))
    pan = db.Column(db.String(20))
    salesman = db.Column(db.String(100))
    blocked = db.Column(db.Boolean, default=False)         # Block (Y/N)
    login_id = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw) if raw else None

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw) if self.password_hash else False


class Product(db.Model):
    """Product / Item Master (Setup > 3. Product Master) — legacy Sheet6/18 'IMC' table."""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)   # IMC
    name = db.Column(db.String(200), nullable=False)  # IMN
    unit = db.Column(db.String(20), default="PCS")
    gst_rate = db.Column(db.Float, default=0)
    hsn_code = db.Column(db.String(20))
    fro = db.Column(db.String(5))   # F=Finished, R=Raw (as seen in original data)
    umrn_code = db.Column(db.String(30))  # legacy UMRN Code field on the Product Master screen
    chassis_item_code = db.Column(db.String(30))  # fixed segment used when generating this product's Chassis No.

    # Form 22 (Road-Worthiness Certificate, CMVR Rule 47(1)(g)) reference data —
    # per-model type-approval details, filled in once per Product from the
    # actual test certificate. Left blank on the printed form if not set here,
    # since these must come from the real certificate, never guessed.
    type_approval_no = db.Column(db.String(60))
    fuel_type = db.Column(db.String(40), default="Battery/Electric")
    horn_db = db.Column(db.String(20))
    pass_by_db = db.Column(db.String(20))


class Vehicle(db.Model):
    """
    Individual manufactured e-rickshaw / e-cart unit (Chassis Master) —
    legacy Sheet4 table. This is the backbone of the Dashboard pipeline view.
    A Vehicle is created by a Production Voucher, and moves through 'stage'
    (Manufacturing -> Delivery Challan -> Tax Invoice) as later vouchers are
    raised against it.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    model_name = db.Column(db.String(200))    # IMN e.g. DAVRATH E-RICKSHAW
    chassis_no = db.Column(db.String(60), unique=True)
    motor_no = db.Column(db.String(60))
    controller_no = db.Column(db.String(60))
    differential_no = db.Column(db.String(60))
    colour = db.Column(db.String(60))
    colour_code = db.Column(db.String(20))
    other = db.Column(db.String(60))

    stage = db.Column(db.String(30), default="Manufacturing")  # Manufacturing / Delivery Challan / Tax Invoice
    dealer_name = db.Column(db.String(200))


class ProductionFormula(db.Model):
    """
    Bill of Material: which raw-material items (and how much of each) go into
    making one unit of a finished product. Legacy Sheet7/22 'PFC/FIMC/RIMC'.
    Each formula has its own `formula_name` (e.g. "jumbo loader"), separate
    from the `product_name` it produces (e.g. "DAVRATH E-LOADER") -- this
    allows more than one named formula/variant to exist for the same
    finished product, mirroring the legacy desktop app's Production Formula
    screen (Setup > 7).
    """
    id = db.Column(db.Integer, primary_key=True)
    formula_name = db.Column(db.String(200), index=True)     # name of the formula itself, e.g. "jumbo loader" -- distinct from the finished product it produces
    product_code = db.Column(db.String(20), index=True)      # PFC
    product_name = db.Column(db.String(200), index=True)     # PFN / FIMN
    raw_item_code = db.Column(db.String(20))                 # RIMC
    raw_item_name = db.Column(db.String(200))                 # RIMN
    qty = db.Column(db.Float, default=1)                       # WT
    unit = db.Column(db.String(20), default="PCS")


class ProductionVoucher(db.Model):
    """
    Production Voucher (Vouchers > D. Production Voucher) — legacy Sheet2/19
    ('VR' == 'W'). Creating one manufactures one finished vehicle (chassis)
    and feeds the Dashboard's "Manufacturing" section.
    """
    id = db.Column(db.Integer, primary_key=True)
    vou_no = db.Column(db.String(20), unique=True)
    date = db.Column(db.Date)

    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    chassis_no = db.Column(db.String(60), unique=True, nullable=False)
    motor_no = db.Column(db.String(60))
    controller_no = db.Column(db.String(60))
    differential_no = db.Column(db.String(60))
    colour = db.Column(db.String(60))
    colour_code = db.Column(db.String(20))
    other = db.Column(db.String(60))

    battery_maker = db.Column(db.String(120))
    battery_no1 = db.Column(db.String(60))
    battery_no2 = db.Column(db.String(60))
    battery_no3 = db.Column(db.String(60))
    battery_no4 = db.Column(db.String(60))

    toolkit = db.Column(db.Boolean, default=True)
    jack = db.Column(db.Boolean, default=True)
    charger = db.Column(db.Boolean, default=True)
    mat = db.Column(db.Boolean, default=True)
    stapney = db.Column(db.Boolean, default=False)
    front_glass = db.Column(db.Boolean, default=False)
    h_lock = db.Column(db.Boolean, default=False)
    center_lock = db.Column(db.Boolean, default=False)

    remarks = db.Column(db.String(300))
    machnic = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("ProductionVoucherItem", backref="voucher",
                             cascade="all, delete-orphan")


class ProductionVoucherItem(db.Model):
    """Raw-material line consumed by a Production Voucher (the BOM actually used)."""
    id = db.Column(db.Integer, primary_key=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey("production_voucher.id"), nullable=False)
    item_code = db.Column(db.String(20))
    item_name = db.Column(db.String(200))
    qty = db.Column(db.Float, default=1)
    unit = db.Column(db.String(20), default="PCS")


class DeliveryChallan(db.Model):
    """
    E-Rickshaw Delivery Challan (Vouchers > E) — legacy Sheet3/10 ('VR' == 'D').
    Moves a manufactured chassis out to a dealer; feeds the Dashboard's
    "Delivery Challan" section until a Tax Invoice is later raised against it.
    """
    id = db.Column(db.Integer, primary_key=True)
    challan_no = db.Column(db.String(20), unique=True)
    date = db.Column(db.Date)
    cancelled = db.Column(db.Boolean, default=False)

    dealer_id = db.Column(db.Integer, db.ForeignKey("dealer.id"))
    dealer = db.relationship("Dealer")
    destination = db.Column(db.String(300))  # end-customer/consignee delivery address, for the printed Warranty Card

    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), unique=True)
    vehicle = db.relationship("Vehicle")

    # snapshot fields (kept even if the vehicle/dealer master record changes later)
    product_name = db.Column(db.String(200))
    chassis_no = db.Column(db.String(60))
    motor_no = db.Column(db.String(60))
    controller_no = db.Column(db.String(60))
    differential_no = db.Column(db.String(60))
    colour = db.Column(db.String(60))
    other = db.Column(db.String(60))

    battery_maker = db.Column(db.String(120))
    battery_no1 = db.Column(db.String(60))
    battery_no2 = db.Column(db.String(60))
    battery_no3 = db.Column(db.String(60))
    battery_no4 = db.Column(db.String(60))

    toolkit = db.Column(db.Boolean, default=True)
    jack = db.Column(db.Boolean, default=True)
    charger = db.Column(db.Boolean, default=True)
    mat = db.Column(db.Boolean, default=True)
    stapney = db.Column(db.Boolean, default=False)
    front_glass = db.Column(db.Boolean, default=False)
    center_lock = db.Column(db.Boolean, default=False)
    h_lock = db.Column(db.Boolean, default=False)

    salesman = db.Column(db.String(100))
    sale_bill_no = db.Column(db.String(30))
    sale_value = db.Column(db.Float, default=0)

    remarks1 = db.Column(db.String(300))
    remarks2 = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TaxInvoice(db.Model):
    """
    Tax Invoice (Vouchers > F) — the GST sale invoice raised against an
    already-delivered chassis. Legacy Sheet2/19 rows ('VR' == 'T'), and the
    printed layout matches `billto.frx` from the original software.

    Saving one moves the chassis to the Dashboard's final "Tax Invoice"
    stage. GST is split CGST+SGST for buyers in the company's home state,
    or charged as IGST for out-of-state buyers, same as the original.
    """
    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(30), unique=True)
    date = db.Column(db.Date)
    cancelled = db.Column(db.Boolean, default=False)

    delivery_challan_id = db.Column(db.Integer, db.ForeignKey("delivery_challan.id"), unique=True)
    delivery_challan = db.relationship("DeliveryChallan")

    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), unique=True)
    vehicle = db.relationship("Vehicle")

    # Buyer details (defaults to the dealer, but can be overridden — the
    # original software lets you bill an end customer instead of the dealer)
    buyer_name = db.Column(db.String(200))
    buyer_relation = db.Column(db.String(10), default="S/o")   # S/o, D/o, W/o, C/o
    buyer_father_name = db.Column(db.String(200))
    buyer_address = db.Column(db.String(300))
    buyer_gst_no = db.Column(db.String(30))
    buyer_pan = db.Column(db.String(20))
    buyer_aadhar = db.Column(db.String(20))
    buyer_mobile = db.Column(db.String(30))
    buyer_state = db.Column(db.String(100))
    buyer_state_code = db.Column(db.String(10))
    # Manual Inside State / Outside State flag (legacy desktop app field) —
    # "I" = Inside state (CGST+SGST) / "O" = Outside state (IGST). Drives the
    # GST split explicitly, same as the original software; falls back to the
    # buyer_state_code comparison below only for older rows saved before
    # this field existed.
    state_type = db.Column(db.String(1), default="I")

    # Buyer date of birth (legacy desktop app field, below Aadhar)
    buyer_dob = db.Column(db.Date)

    # Vehicle snapshot (from the Delivery Challan / Vehicle)
    dealer_name = db.Column(db.String(200))
    product_name = db.Column(db.String(200))
    chassis_no = db.Column(db.String(60))
    motor_no = db.Column(db.String(60))
    controller_no = db.Column(db.String(60))
    other_desc = db.Column(db.String(60))
    colour = db.Column(db.String(60))

    # Amounts
    # Two distinct amounts, matching the legacy desktop form: "Sale Amount"
    # (internal — the actual/agreed dealer sale price, used for internal
    # records) and "Amount" (the GST/taxable basis the invoice tax is
    # calculated on). They're often the same, but not always.
    sale_amount = db.Column(db.Float, default=0)       # internal sale amount
    gst_sale_amount = db.Column(db.Float, default=0)   # GST taxable-value basis
    discount = db.Column(db.Float, default=0)
    gst_rate = db.Column(db.Float, default=5)          # total GST %, split if intra-state
    insurance_amount = db.Column(db.Float, default=0)
    registration_amount = db.Column(db.Float, default=0)

    # Financer / Hypothecation
    financer_name = db.Column(db.String(200))
    hypothecation_amount = db.Column(db.Float, default=0)

    # Payment tracking (Reports > U. Payment Rec'able Report)
    amount_received = db.Column(db.Float, default=0)
    # Government subsidy applicable to this sale (Reports > V. Subsidy Report)
    subsidy_amount = db.Column(db.Float, default=0)
    # Subsidy claim status, set from the Payment Details popup: Due (not yet
    # claimed) / Submit (claim submitted) / Reject (claim rejected) / Paid
    subsidy_status = db.Column(db.String(20), default="Due")

    # RTO / dispatch
    rto_name = db.Column(db.String(120))
    vehicle_reg_no = db.Column(db.String(30))
    despatch_through = db.Column(db.String(120))
    eway_bill_no = db.Column(db.String(40))

    # Mode / Term of payment (legacy desktop app field, e.g. "BANK/CASH")
    mode_term = db.Column(db.String(40), default="BANK/CASH")
    bank_name = db.Column(db.String(120))
    bank_account_no = db.Column(db.String(50))
    bank_ifsc = db.Column(db.String(50))
    cvr_no = db.Column(db.String(40))
    license_no = db.Column(db.String(40))
    cancelled_cheque_no = db.Column(db.String(40))
    remarks = db.Column(db.String(300))

    # Legacy accounting cross-references (old system's LEDGER/VOUNO/CHASSISREC
    # columns) -- carried over as plain reference fields, not used elsewhere.
    ledger_no = db.Column(db.String(40))
    voucher_no = db.Column(db.String(40))
    chassis_record_no = db.Column(db.String(40))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_inter_state(self):
        # Legacy desktop app drives this off the manual Inside/Outside State
        # flag rather than comparing state codes. Fall back to the state-code
        # comparison for older rows saved before that flag existed.
        if self.state_type:
            return self.state_type == "O"
        # Company home state code is Delhi ("07"), matching the sample invoice's GSTIN 07xxxxx
        return bool(self.buyer_state_code) and self.buyer_state_code != "07"

    @property
    def taxable_value(self):
        base = self.gst_sale_amount if self.gst_sale_amount else self.sale_amount
        return round((base or 0) - (self.discount or 0), 2)

    @property
    def igst_amount(self):
        return round(self.taxable_value * (self.gst_rate or 0) / 100, 2) if self.is_inter_state else 0

    @property
    def cgst_amount(self):
        return round(self.taxable_value * (self.gst_rate or 0) / 200, 2) if not self.is_inter_state else 0

    @property
    def sgst_amount(self):
        return self.cgst_amount if not self.is_inter_state else 0

    @property
    def tax_amount(self):
        return self.igst_amount if self.is_inter_state else (self.cgst_amount + self.sgst_amount)

    @property
    def bill_total(self):
        return round(self.taxable_value + self.tax_amount +
                      (self.insurance_amount or 0) + (self.registration_amount or 0), 2)

    @property
    def balance_due(self):
        return round(self.bill_total - (self.hypothecation_amount or 0) - (self.amount_received or 0), 2)

    @property
    def payment_status(self):
        if self.balance_due <= 0:
            return "Paid"
        elif (self.amount_received or 0) > 0:
            return "Partial"
        return "Due"


class PurchaseBill(db.Model):
    """
    Purchase Bill (Vouchers > C) — recording a raw-material purchase from a
    party. Legacy Sheet2/19 rows ('VR' == blank/'P'), feeding the Purchase
    Register report. Independent of the vehicle pipeline (raw materials
    don't move through the Dashboard stages).
    """
    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(30))
    date = db.Column(db.Date)

    party_name = db.Column(db.String(200), nullable=False)
    party_gst_no = db.Column(db.String(30))
    party_state_code = db.Column(db.String(10), default="07")

    remarks = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("PurchaseBillItem", backref="bill", cascade="all, delete-orphan")

    @property
    def is_inter_state(self):
        return bool(self.party_state_code) and self.party_state_code != "07"

    @property
    def taxable_total(self):
        return round(sum(i.taxable_amt for i in self.items), 2)

    @property
    def tax_total(self):
        return round(sum(i.tax_amt for i in self.items), 2)

    @property
    def bill_total(self):
        return round(self.taxable_total + self.tax_total, 2)


class PurchaseBillItem(db.Model):
    """One raw-material line within a Purchase Bill."""
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("purchase_bill.id"), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    hsn_code = db.Column(db.String(20))
    qty = db.Column(db.Float, default=1)
    rate = db.Column(db.Float, default=0)
    gst_rate = db.Column(db.Float, default=0)

    @property
    def taxable_amt(self):
        return round((self.qty or 0) * (self.rate or 0), 2)

    @property
    def is_inter_state(self):
        return self.bill.is_inter_state if self.bill else False

    @property
    def igst_amt(self):
        return round(self.taxable_amt * (self.gst_rate or 0) / 100, 2) if self.is_inter_state else 0

    @property
    def cgst_amt(self):
        return round(self.taxable_amt * (self.gst_rate or 0) / 200, 2) if not self.is_inter_state else 0

    @property
    def sgst_amt(self):
        return self.cgst_amt if not self.is_inter_state else 0

    @property
    def tax_amt(self):
        return self.igst_amt if self.is_inter_state else (self.cgst_amt + self.sgst_amt)


class OldRickshaw(db.Model):
    """
    Old Rickshaw (Vouchers > G) — buy-back / trade-in of a used e-rickshaw.
    Legacy Sheet8/27 ('VR' == 'O'). Tracked by vehicle registration number
    (not chassis), independent of the new-manufacture pipeline since it's a
    used vehicle already registered with the RTO.
    """
    id = db.Column(db.Integer, primary_key=True)
    vou_no = db.Column(db.String(20))
    date = db.Column(db.Date)

    party_name = db.Column(db.String(200))       # AMN — ledger/account this is booked against
    vehicle_reg_no = db.Column(db.String(30))     # VEHNO
    model_name = db.Column(db.String(200))         # IMN
    owner_name = db.Column(db.String(200))         # ONAME — person who owned/sold it
    salesman = db.Column(db.String(100))            # SNAME

    sold_amount = db.Column(db.Float, default=0)     # SOLDAMT
    loan_amount = db.Column(db.Float, default=0)      # LOANAMT
    receipt_amount = db.Column(db.Float, default=0)    # RCPTAMT
    receipt_no = db.Column(db.String(30))               # RNO
    ledger = db.Column(db.String(200))

    resale_date = db.Column(db.Date)               # SDT — if/when resold
    resale_ledger = db.Column(db.String(200))

    remarks1 = db.Column(db.String(300))
    remarks2 = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def balance_amount(self):
        return round((self.sold_amount or 0) - (self.receipt_amount or 0), 2)


class BatteryDeliveryChallan(db.Model):
    """
    Battery Delivery Challan (Vouchers > H) — a battery sent to a dealer on
    its own (e.g. a warranty replacement), separate from a full vehicle
    Delivery Challan.
    """
    id = db.Column(db.Integer, primary_key=True)
    challan_no = db.Column(db.String(20), unique=True)
    date = db.Column(db.Date)

    dealer_id = db.Column(db.Integer, db.ForeignKey("dealer.id"))
    dealer = db.relationship("Dealer")

    battery_maker = db.Column(db.String(120))
    battery_no = db.Column(db.String(60))
    qty = db.Column(db.Integer, default=1)
    remarks = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class JournalStock(db.Model):
    """
    Journal Stock (Vouchers > I) — a manual stock correction/adjustment
    (raw material or finished item) that doesn't come from a Purchase Bill,
    Production Voucher, or Delivery Challan — e.g. fixing a stock-take
    discrepancy. Positive qty increases stock, negative qty decreases it.
    """
    id = db.Column(db.Integer, primary_key=True)
    vou_no = db.Column(db.String(20))
    date = db.Column(db.Date)
    item_name = db.Column(db.String(200), nullable=False)
    item_type = db.Column(db.String(10), default="R")   # R=Raw Material, F=Finished Good
    qty = db.Column(db.Float, default=0)                   # +in / -out
    reason = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DayBook(db.Model):
    """
    Day Book Entry (Reports > W. Ledger > Day Book Entry) — a manual
    receipt/payment voucher against a dealer/party, matching the original
    software's Day Book screen. Not tied to a Tax Invoice; used for
    recording bank transfers, UPI/NEFT receipts, cheques paid out, etc.
    Has its own Vr.No. sequence, separate from other voucher types.
    Feeds into the party Ledger (W. Ledger) alongside Tax Invoice events.
    """
    id = db.Column(db.Integer, primary_key=True)
    vr_no = db.Column(db.Integer, unique=True)          # Day Book's own running voucher number
    date = db.Column(db.Date)
    dealer_name = db.Column(db.String(200), nullable=False)   # free-text party name, as in the original
    credit_received = db.Column(db.Float, default=0)   # money received from the party (reduces balance due)
    debit_paid = db.Column(db.Float, default=0)        # money paid out to the party (increases balance due)
    narration = db.Column(db.String(500))               # e.g. "UPI 1525", "V C NO-2939 (RAJ KUMAR)"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def next_vr_no():
        last = DayBook.query.order_by(DayBook.vr_no.desc()).first()
        return (last.vr_no + 1) if last and last.vr_no else 1


class User(db.Model):
    """App login user — legacy Sheet23 'uid/pw' table, but with proper hashing here."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_super_user = db.Column(db.Boolean, default=False)   # su == 'S'
    permissions = db.Column(db.String(50))                  # per, e.g. "Y Y"
    allowed_modules = db.Column(db.Text)                    # comma-separated menu-item keys this user may access
                                                              # (ignored for super users, who always see everything)

    def has_module_access(self, key):
        if self.is_super_user:
            return True
        if not self.allowed_modules:
            return False
        return key in self.allowed_modules.split(",")

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)
