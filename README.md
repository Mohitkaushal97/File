# files
- bs.sh - bootstrap.sh , initialize Ubuntu 18.04 setup
- bs_docker.sh - Docker bootstrap, e.g. install Docker on Ubuntu 18.04 system

run these 2 files to setup Ubuntu 18.04 machine::
```
bash bs.sh
bash bs_docker.sh
```
 
# Running
## Run with Docker

with docker:: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html
```
# copy configuration from heroku config to environment varibles
source export_conf.sh

# verify config (use -E to inherit env vars when sudo)
sudo -E docker-compose -f local.yml config
# spcifically, verify this field:
sudo -E docker-compose -f local.yml config | egrep "API__SERVER_WITH_PORT"

# build and run (use "-d" to run in the background) ; don't forget -E if required
sudo -E docker-compose -f local.yml build
sudo -E docker-compose -f local.yml up

# run in background:
sudo -E docker-compose -f local.yml up -d
# stop running in background:
sudo -E docker-compose -f local.yml down


create super user:
sudo -E docker-compose -f local.yml run --rm django  python3 manage.py setup_admin -u=danny -p=danny1234 -e=danny.123@example.com

sudo -E docker-compose -f local.yml run --rm django python3 manage.py collectstatic
```


### Run commands in docker:
```
sudo -E docker-compose -f local.yml run --rm django python manage.py makemigrations 
sudo -E docker-compose -f local.yml run --rm django python manage.py migrate
 
sudo -E docker-compose -f local.yml run --rm django python3 manage.py setup_admin -u=danny -p=danny1234 -e=danny.123@example.com
sudo -E docker-compose -f local.yml run --rm django init_data

sudo -E docker-compose -f local.yml run --rm django pytest
```

## Run commands on Heroku
run commands on Heroku:
```
heroku run python manage.py makemigrations
heroku run python manage.py migrate

heroku run python manage.py setup_admin -u=danny -p=danny1234 -e=danny.123@gmail.com
heroku run python manage.py init_data

heroku run python pytest # CURRENTLY NOT WORKING!!
```

For manual see:
```
https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax
```

