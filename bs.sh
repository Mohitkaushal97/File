#!/usr/bin/bash

echo "general system setup"


# general installs
sudo apt update
sudo apt-get update
sudo yum update -y

sudo apt-get install -y python-dev   # for python2.x installs  - Ubuntu, Debian
sudo apt-get install -y python3-dev   # Ubuntu, Debian
sudo yum install -y python-devel   # for python2.x installs - CentOS, RHEL
sudo yum install -y python3-devel   # CentOS, RHEL

# postgres stuff
# when deploying to Heroku, it uses alpine and it installs "apk add postgresql-dev"
https://stackoverflow.com/a/28938258
sudo apt-get install -y python-psycopg2
sudo apt-get install -y libpq-dev

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
sudo python -m pip install --upgrade pip

# install & upgrade pip - Python 3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo apt-get install -y python3-distutils # Ubuntu 18 required
sudo python3 get-pip.py
sudo python3 -m pip install --upgrade pip

# another method
sudo apt install -y python-pip python-virtualenv
sudo apt install -y python3-pip python3-virtualenv
sudo python3 -m pip install --upgrade pip


# install cookiecutter for Python3 only!! We must not have it for Python2, since it can make troubles
sudo python2 -m pip uninstall cookiecutter==1.6.0
sudo python3 -m pip install cookiecutter==1.6.0


# https://github.com/chargebee/chargebee-python
pip install 'chargebee>=2,<3'
