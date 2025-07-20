import json
import os
from pathlib import Path


class AppSettings:
    APP_SETTINGS: dict = None

    def __init__(self):
        AppSettings.APP_SETTINGS = {}
        self._dir = os.path.join(Path(__file__).resolve().parent.parent.parent.parent, "crm_optimized")
        self._read_settings()

    def _read_settings(self):
        with open(os.path.join(self._dir, 'app_settings.json'), 'r') as f:
            AppSettings.APP_SETTINGS = json.load(f)