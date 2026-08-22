import pyodbc

filepath = r"I:\Projects\eBILL.mdb"
password = "JAISHREE@$GANESH"

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={filepath};"
    rf"PWD={password};"
)
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

print("=== INV: VR breakdown ===")
cursor.execute("SELECT VR, COUNT(*) FROM INV GROUP BY VR")
for row in cursor.fetchall():
    print(repr(row[0]), row[1])

print()
print("=== BDCH: sample row ===")
cursor.execute("SELECT * FROM BDCH")
cols = [c[0] for c in cursor.description]
for row in cursor.fetchall():
    print(dict(zip(cols, row)))

print()
print("=== VEHOLD: VR breakdown ===")
cursor.execute("SELECT VR, COUNT(*) FROM VEHOLD GROUP BY VR")
for row in cursor.fetchall():
    print(repr(row[0]), row[1])

print()
print("=== INV: one sample row per VR value ===")
cursor.execute("SELECT DISTINCT VR FROM INV")
vr_values = [row[0] for row in cursor.fetchall()]
for vr in vr_values:
    cursor.execute("SELECT TOP 1 * FROM INV WHERE VR = ?", vr) if vr is not None else cursor.execute("SELECT TOP 1 * FROM INV WHERE VR IS NULL")
    cols = [c[0] for c in cursor.description]
    r = cursor.fetchone()
    print(f"\n--- VR={vr!r} ---")
    if r:
        print(dict(zip(cols, r)))

conn.close()