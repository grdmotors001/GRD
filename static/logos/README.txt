Drop model/brand logo images here.

Naming: name each file after the model's UMRN Code or Item Code exactly as
entered in Setup > Product Master (e.g. "DAVRATH01.jpg"). The Delivery
Challan print view looks for a file matching the product's UMRN Code first,
then its Chassis Item Code, then the product name itself — whichever one
matches a file here gets used, checking .jpg / .jpeg / .png / .webp in
that order.

_default.png is a placeholder logo shown when no product-specific match is
found, so the print preview always has a visible logo slot instead of a
blank gap. Replace _default.png with a real fallback/company logo any time,
or add per-product files (named as above) to override it for specific
models.
