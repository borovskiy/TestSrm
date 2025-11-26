http://localhost:8080/
http://localhost:8089/
http://localhost:5050/docs

export DATABASE_URL="postgresql+asyncpg://alchemy_user:strong_password_123@localhost:5432/alchemy_crm"
alembic revision --autogenerate
alembic upgrade head


SELECT * FROM public.users;
SELECT * FROM public.tasks;
SELECT * FROM public.organizations;
SELECT * FROM public.organization_members;
SELECT * FROM public.deals;
SELECT * FROM public.contacts;
SELECT * FROM public.alembic_version;
SELECT * FROM public.activities;

docker compose --env-file ./app/.env up -d
docker compose --env-file ./app/.env down