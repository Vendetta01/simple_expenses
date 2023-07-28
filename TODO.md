# TODO

* [X] Create import for category mappings
* [X] Set own postgres as db
* [X] Create interface to select a list of transactions that should be set to a category
* [ ] Maybe implement some logic to guess the category?
* [X] Set up git
* [ ] Integrate into docker-composition-home
* [X] Change entrypoint script to use gunicorn again (for that we need a proxy that serves the static files)
* [ ] Get env variable ALLOWED_HOSTS to work properly (right now we get a json decode error...), we need this to properly integrate into docker_composition_home
* [ ] Write tests
* [ ] Create github actions to run tests and maybe create docker image on push
* [X] Add whitenoise as static files server
