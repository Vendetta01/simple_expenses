# TODO

* [X] Create import for category mappings
* [X] Set own postgres as db
* [X] Create interface to select a list of transactions that should be set to a category
* [ ] Maybe implement some logic to guess the category?
* [X] Set up git
* [X] Integrate into docker-composition-home
* [X] Change entrypoint script to use gunicorn again (for that we need a proxy that serves the static files)
* [X] Get env variable ALLOWED_HOSTS to work properly (right now we get a json decode error...), we need this to properly integrate into docker_composition_home
* [ ] Write tests
* [ ] Create github actions to run tests and maybe create docker image on push
* [X] Add whitenoise as static files server
* [ ] Look into Metabase Actions, can this be used to bulk update? Then we could reduce this to a simple ORM + import/export scripts
* [X] Add new column "comment" to transactions so that we can add information that is not deductible from the purpose field
* [X] Category should be printed as complete hierarchy
* [ ] Add checks to load of categories
* [X] Add atomic operation so that either import succeeds or fails completely
* [X] Remove default admin delete action