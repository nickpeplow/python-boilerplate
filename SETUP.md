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


## Tailwind CSS Setup

1. Install Node.js and npm if you don't have them:
   - Download from [nodejs.org](https://nodejs.org/)
   - Or use a package manager: `brew install node` (macOS), `apt install nodejs npm` (Ubuntu)

2. Install Tailwind CSS and its dependencies:
   ```bash
   # Make sure you're in the project root
   npm install
   ```

3. Build the Tailwind CSS file:
   ```bash
   # For production (minified)
   npm run build
   
   # For development (with watch mode)
   npm run dev
   ```

## Development Workflow

1. Run the Flask application in one terminal:
   ```bash
   python3.10 app.py
   ```

2. Run Tailwind in watch mode in another terminal:
   ```bash
   npm run dev
   ```

3. Make changes to your templates and Tailwind will automatically regenerate the CSS.
