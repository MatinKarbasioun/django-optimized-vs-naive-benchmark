import uuid

from crm.application.utils.app_settings import AppSettings


def generate_customer_id() -> str:
    return f"{AppSettings.APP_SETTINGS['business']['customer_id_prefix']}:{uuid.uuid4().hex}"