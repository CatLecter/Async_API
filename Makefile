test:
	docker-compose -f tests/functional/docker-compose.yml up -d
	sleep 30
	pytest tests/functional/src/

dev:
	docker-compose -f docker-compose.dev.yml up -d --build

prod:
	docker-compose -f docker-compose.yml down -v
	docker-compose -f docker-compose.yml up -d --build
	docker-compose -f docker-compose.yml exec admin_panel python manage.py collectstatic --no-input --clear
	docker-compose -f docker-compose.yml exec admin_panel python manage.py migrate --fake movies 0001
	docker-compose -f docker-compose.yml exec admin_panel python manage.py makemigrations
	docker-compose -f docker-compose.yml exec admin_panel python manage.py migrate
	docker-compose -f docker-compose.yml exec admin_panel python manage.py createsuperuser --noinput
	docker-compose -f docker-compose.yml exec admin_panel python manage.py loaddata /home/app/fixtures.json.gz

create_env:
	cp -f deploy/admin_panel/example.env deploy/admin_panel/.env
	cp -f deploy/db/example.env deploy/db/.env
	cp -f deploy/ps_to_es/example.env deploy/ps_to_es/.env
