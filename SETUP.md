git remote add -f np-boilerplate https://github.com/nickpeplow/python-boilerplate.git

# Create a new virtual environment
python3 -m venv fresh_venv

# Activate it
source fresh_venv/bin/activate

pip install -r boilerplate/requirements.txt

python3 app.py

flask db init