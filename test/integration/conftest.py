DB = {
    "host": "localhost",
    "port": "5432",
    "dbname": "main_db",
    "user": "robot",
    "password": "any_password_replaced_later",
}

DB_USER_REGULAR = (
    f"postgres://{DB['user']}:"
    f"{DB['password']}@"
    f"{DB['host']}:"
    f"{DB['port']}:"
    f"{DB['dbname']}?sslmode=disable"
)

DB_USER_ROOT = (
    "postgres://postgres:"
    "postgres@"
    f"{DB['host']}:"
    f"{DB['port']}:"
    f"{DB['dbname']}?sslmode=disable"
)
