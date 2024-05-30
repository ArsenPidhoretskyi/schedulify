.ONESHELL:

install:
	poetry install --with dev --no-root

lock:
	poetry lock

test:
	pytest --no-migrations

test-coverage:
	pytest --no-migrations --cov=schedulify --cov-report term-missing:skip-covered

check-migrations:
	python manage.py makemigrations --check --dry-run

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

check:
	black . --check \
	&& ruff check . \
	&& safety check \
	&& make check-migrations \

check-fix:
	black .
	ruff check --fix-only --show-fixes --statistics .

run:migrate collectstatic
	python manage.py runserver_plus 0.0.0.0:8000 --nostatic

celery-worker-run:
	celery -A schedulify worker

celery-beat-run:
	celery -A schedulify beat
