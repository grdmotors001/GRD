import pyodbc

filepath = r"I:\Projects\eBILL.mdb"
password = "JAISHREE@$GANESH"

print("Password Python sees:", repr(password))

try:
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={filepath};"
        rf"PWD={password};"
    )
    conn = pyodbc.connect(conn_str, autocommit=True)
    print("Try 1 (PWD only): CONNECTED OK")
    conn.close()
except pyodbc.Error as e:
    print("Try 1 (PWD only) FAILED:", e)

try:
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={filepath};"
        r"UID=Admin;"
        rf"PWD={password};"
    )
    conn = pyodbc.connect(conn_str, autocommit=True)
    print("Try 2 (UID=Admin + PWD): CONNECTED OK")
    conn.close()
except pyodbc.Error as e:
    print("Try 2 (UID=Admin + PWD) FAILED:", e)