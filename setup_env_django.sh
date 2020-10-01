python3 -m venv venv_jobs_djan/
source venv_jobs_djan/bin/activate
# install wheel; otherwise have to install requirements twice
pip install wheel

python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt # just in case..

