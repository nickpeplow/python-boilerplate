git remote add -f main https://github.com/nickpeplow/python-boilerplate.git

git pull main main

# Create a new virtual environment
python3 -m venv fresh_venv

# Activate it
source fresh_venv/bin/activate

pip install -r boilerplate/requirements.txt

python3 app.py

flask db init

--

Menu is in project/config.py

Heroku
heroku ps:scale web=1 -a np-attribution