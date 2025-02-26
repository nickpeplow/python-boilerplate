import click
from flask.cli import with_appcontext
from boilerplate.database import db
from project.example.models import Example

@click.command('generate-examples')
@with_appcontext
def generate_examples_command():
    """Generate example data for testing."""
    click.echo('Generating example data...')
    
    # Create some example data
    from project.example.services import ExampleService
    from flask_login import current_user
    
    # This is just a placeholder - in a real command you'd create actual data
    example_data = {
        'name': 'Sample Example',
        'description': 'This is a sample example created by the CLI command'
    }
    
    # Note: Since this is run from CLI, there's no current_user
    # You would need to specify a user ID or create a system user
    try:
        # For demonstration only - this won't work without a user_id
        # ExampleService.create_example(1, example_data)  # Using user_id 1
        click.echo('Example data would be created here (disabled for safety)')
    except Exception as e:
        click.echo(f'Error generating example data: {str(e)}')
    
    click.echo('Done.')

# Remove or comment out these imports and commands since they reference the removed topical_map module
# @click.command('generate-categories')
# @with_appcontext
# def generate_categories_command():
#     """Generate categories for testing."""
#     click.echo('This command has been removed.')

# @click.command('generate-subtopics')
# @with_appcontext
# def generate_subtopics_command():
#     """Generate subtopics for testing."""
#     click.echo('This command has been removed.') 