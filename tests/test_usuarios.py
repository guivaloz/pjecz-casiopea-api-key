"""
Unit tests usuarios
"""

import unittest

import requests

from tests import config


class TestUsuarios(unittest.TestCase):
    """Test usuarios"""

    def test_get_usuarios(self):
        """Test GET method for usuarios"""
        response = requests.get(
            f"{config['api_base_url']}/usuarios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue("success" in payload)
        self.assertTrue(payload["success"])
        self.assertTrue("message" in payload)
        self.assertTrue("data" in payload)
        self.assertTrue(isinstance(payload["data"], list))
        for item in payload["data"]:
            self.assertTrue("email" in item)
            self.assertTrue("nombres" in item)
            self.assertTrue("apellido_paterno" in item)
            self.assertTrue("apellido_materno" in item)
            self.assertTrue("puesto" in item)


if __name__ == "__main__":
    unittest.main()
