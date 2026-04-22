import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Fail fast if critical secrets are missing
required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]

for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")
