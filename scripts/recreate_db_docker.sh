#!/bin/bash
set -euo pipefail


# rm db.sqlite3
docker-compose exec web bash -c "python manage.py sqlflush | python manage.py dbshell"
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser --email nils.podewitz@googlemail.com --username admin

docker-compose exec web python manage.py import --source categories "/data/input/categories/*.csv"
docker-compose exec web python manage.py import --encoding "ISO8859-15" --skip-lines 4 "/data/input/norisbank/*.csv"

