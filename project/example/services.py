from .models import Example
from boilerplate.database import db
from flask import current_app

class ExampleService:
    @staticmethod
    def get_example(example_id, user_id):
        return Example.query.filter_by(id=example_id, user_id=user_id).first()

    @staticmethod
    def get_user_examples(user_id):
        return Example.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_example(user_id, data):
        example = Example(
            user_id=user_id,
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(example)
        db.session.commit()
        return example

    @staticmethod
    def update_example(example, data):
        example.name = data['name']
        example.description = data.get('description')
        db.session.commit()
        return example

    @staticmethod
    def delete_example(example):
        """Delete an example"""
        try:
            db.session.delete(example)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to delete example: {str(e)}") 