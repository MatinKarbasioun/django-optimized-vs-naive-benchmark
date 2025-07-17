__all__ = [
    'handle_db_operation',
    'CustomNinjaAPI',
    'CustomSwagger'
]

from .django_ninja import CustomNinjaAPI, CustomSwagger
from .db_operation_handler import handle_db_operation