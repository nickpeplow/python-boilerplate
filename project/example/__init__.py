from flask import Blueprint

example_bp = Blueprint('example', __name__, 
    template_folder='templates',
    url_prefix='/examples'
)

# Import routes after blueprint creation to avoid circular imports
from . import routes 