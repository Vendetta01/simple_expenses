# TODO

* [X] Create import for category mappings
* [X] Set own postgres as db
* [X] Create interface to select a list of transactions that should be set to a category
* [ ] Maybe implement some logic to guess the category?
* [X] Set up git
* [ ] Integrate into docker-composition-home
* [ ] Change entrypoint script to use gunicorn again (for that we need a proxy that serves the static files)
* [ ] Get env variable ALLOWED_HOSTS to work properly (right now we get a json decode error...)