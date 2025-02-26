from flask import Blueprint

auth_bp = Blueprint('auth', __name__, 
    template_folder='templates'
)

# Import routes at the bottom of __init__.py
from . import routes 