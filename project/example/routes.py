from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import example_bp
from .forms import ExampleForm
from .services import ExampleService
import logging
from functools import wraps

logger = logging.getLogger(__name__)
example_service = ExampleService()

class ExampleError(Exception):
    """Custom exception for example-related errors"""
    pass

def handle_example_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Example error: {str(e)}")
            flash(str(e), 'error')
        except ExampleError as e:
            logger.error(f"Example operation failed: {str(e)}")
            flash(str(e), 'error')
        except Exception as e:
            logger.exception("Unexpected error in example blueprint")
            flash(str(e), 'error')
        return redirect(url_for('example.list'))
    return wrapper

@example_bp.route('/')
@login_required
def index():
    return redirect(url_for('example.list'))

@example_bp.route('/list')
@login_required
@handle_example_error
def list():
    examples = example_service.get_user_examples(current_user.id)
    return render_template('example/list.html', examples=examples)

@example_bp.route('/manage', defaults={'example_id': None}, methods=['GET', 'POST'])
@example_bp.route('/manage/<int:example_id>', methods=['GET', 'POST'])
@login_required
@handle_example_error
def manage(example_id):
    example = example_service.get_example(example_id, current_user.id) if example_id else None
    form = ExampleForm(obj=example)
    
    if request.method == 'POST' and form.validate():
        try:
            data = {
                'name': form.name.data,
                'description': form.description.data
            }
            
            if example:
                example_service.update_example(example, data)
                new_example = example
            else:
                new_example = example_service.create_example(current_user.id, data)
            
            flash('Example saved successfully', 'success')
            return redirect(url_for('example.details', example_id=new_example.id))
            
        except Exception as e:
            logger.exception("Error saving example")
            flash(f"Error saving example: {str(e)}", 'error')
            return render_template('example/manage.html', form=form, example=example)
    
    return render_template('example/manage.html', form=form, example=example)

@example_bp.route('/<int:example_id>')
@login_required
@handle_example_error
def details(example_id):
    example = example_service.get_example(example_id, current_user.id)
    if not example:
        flash('Example not found', 'error')
        return redirect(url_for('example.list'))
        
    return render_template('example/details.html', example=example)

@example_bp.route('/<int:example_id>/delete', methods=['POST'])
@login_required
@handle_example_error
def delete(example_id):
    example = example_service.get_example(example_id, current_user.id)
    if not example:
        flash('Example not found', 'error')
        return redirect(url_for('example.list'))
    
    try:
        example_service.delete_example(example)
        flash('Example deleted successfully', 'success')
    except ValueError as e:
        flash(str(e), 'error')
        
    return redirect(url_for('example.list')) 