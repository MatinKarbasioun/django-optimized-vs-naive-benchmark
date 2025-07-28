import logging
from typing import Type, Any, Optional, Callable, Awaitable

from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError
from django.db.models import Model

from shared.exception import InvalidDataException

logger = logging.getLogger(__name__)

async def handle_db_operation(operation_func: Callable[[], Awaitable[Any]],
                      custom_exception: Type[Exception] = InvalidDataException,
                      custom_message: Optional[str] = None) -> Any:

    try:
        return await operation_func()

    except IntegrityError as e:
        error_msg = f"{str(operation_func)} failed due to data constraint violation"
        logger.error(f"{error_msg}: {e}")
        raise custom_exception(f"{error_msg}: {e}") from e

    except ValidationError as e:
        error_msg = custom_message or f"{str(operation_func)} failed due to validation error"
        logger.error(f"{error_msg}: {e}")
        raise custom_exception(f"{error_msg}: {e}") from e

    except DataError as e:
        error_msg = custom_message or f"{str(operation_func)} failed due to data error"
        logger.error(f"{error_msg}: {e}")
        raise custom_exception(f"{error_msg}: {e}") from e

    except Model.DoesNotExist as e:
        error_msg = custom_message or f"{str(operation_func)} model doesn't exist"
        logger.error(f"{error_msg}: {e}")
        return None

    except Exception as e:
        error_msg = custom_message or f"{str(operation_func)} failed"
        logger.error(f"{error_msg}: {e}")
        raise custom_exception(f"{error_msg}: {e}") from e

