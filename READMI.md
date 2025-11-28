

# CRM System

## Описание

Это CRM система, разработанная с использованием Python и FastAPI.  Она предоставляет следующие основные функции:

*   Управление организациями
*   Управление контактами
*   Управление сделками
*   Управление задачами
*   Управление активностями
*   Авторизация

## Технологии

*   Python
*   FastAPI
*   PostgreSQL
*   Docker
*   Alembic

## Запуск проекта

### Запуск с помощью Docker Compose

1.  Убедитесь, что у вас установлен Docker и Docker Compose.
2.  Перейдите в каталог проекта.
3.  Запустите:

```bash
docker compose --env-file ./app/.env up -d
```

### Запуск Alembic

```bash
alembic revision --autogenerate
alembic upgrade head
```

### Остановка с помощью Docker Compose

```bash
docker compose --env-file ./app/.env down
```

## API Endpoints

*   /api/v1/organisation/me
*   /api/v1/contacts/list
*   /api/v1/deals/list
*   /api/v1/tasks/
*   /api/v1/deals/1/activities

##  Тестирование

Для запуска тестов используйте pytest:

```bash
pytest tests
```

##  Дополнительная информация


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