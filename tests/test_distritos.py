"""
Unit tests distritos
"""

import unittest

import requests

from tests import config


class TestDistritos(unittest.TestCase):
    """Test distritos"""

    def test_get_distritos(self):
        """Test GET distritos"""
        response = requests.get(
            url=f"{config['api_base_url']}/distritos",
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
            self.assertTrue("clave" in item)
            self.assertTrue("nombre" in item)
            self.assertTrue("nombre_corto" in item)
            self.assertTrue("es_jurisdiccional" in item)


if __name__ == "__main__":
    unittest.main()
