#!/bin/bash
set -euo pipefail


rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser --email nils.podewitz@googlemail.com --username admin

python manage.py import --source categories "../data/categories/*.csv"
python manage.py import --encoding "ISO8859-15" --skip-lines 4 "../data/norisbank/*.csv"

