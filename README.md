# Blog 

This blog was made in the course Python of Otavio Miranda

# Comands Docker Compose

Example:
* Build the container: docker-compose up --build
* Reset containers: docker-compose up --build --remove-orphans --renew-anon-volumes --force-recreate
* Up the application: docker-compose up
* Execute commands py: docker-compose run --rm djangoapp python manage.py makemigrations
* Execute Scripts: docker-compose run --rm djangoapp 'name-script-file'