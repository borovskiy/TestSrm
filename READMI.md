http://localhost:8080/
http://localhost:8089/
http://localhost:5050/docs

export DATABASE_URL="postgresql+asyncpg://alchemy_user:strong_password_123@localhost:5432/alchemy_crm"
alembic upgrade head


docker compose --env-file ./app/.env up -d
docker compose --env-file ./app/.env down