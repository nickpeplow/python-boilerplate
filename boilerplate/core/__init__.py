from flask import Blueprint, request

core_bp = Blueprint('core', __name__, 
    template_folder='templates'
)

def is_route_active(route):
    """Check if the given route matches the current request endpoint"""
    return request.endpoint.startswith(route) if request.endpoint else False

# Make the function available to templates
core_bp.add_app_template_global(is_route_active, 'is_route_active') 