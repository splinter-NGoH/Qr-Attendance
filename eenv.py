import os

# os.environ["DATABASE_URL"] = "postgres://postgres:Casherboy1@127.0.0.1:5432/qr_code"

print(os.getenv("DJANGO_SECRET_KEY"))
