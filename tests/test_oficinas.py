"""
Unit tests oficinas
"""

import unittest

import requests

from tests import config


class TestOficinas(unittest.TestCase):
    """Test oficinas"""

    def test_get_oficinas(self):
        """Test GET method for oficinas"""
        response = requests.get(
            url=f"{config['api_base_url']}/oficinas",
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
            self.assertTrue("domicilio_edificio" in item)
            self.assertTrue("clave" in item)
            self.assertTrue("descripcion" in item)
            self.assertTrue("descripcion_corta" in item)


if __name__ == "__main__":
    unittest.main()
