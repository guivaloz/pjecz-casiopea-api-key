"""
Tests Init
"""

import os
import uuid

from dotenv import load_dotenv

load_dotenv()


def fake_curp() -> str:
    """Genera un CURP inexistente para pruebas"""
    return "XXXX900101XXXXXX00"


def fake_uuid() -> str:
    """Genera un UUID aleatorio para pruebas"""
    return str(uuid.uuid4())


config = {
    "api_key": os.getenv("API_KEY", ""),
    "api_base_url": os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v5"),
    "curp": os.getenv("CURP", fake_curp()),
    "cit_cliente_id": os.getenv("CIT_CLIENTE_ID", fake_uuid()),
    "timeout": int(os.getenv("TIMEOUT", "10")),
}
