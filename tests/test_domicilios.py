"""
Unit tests domicilios
"""

import unittest

import requests

from tests import config


class TestDomicilios(unittest.TestCase):
    """Test domicilios"""

    def test_get_domicilios(self):
        """Test GET domicilios"""
        response = requests.get(
            url=f"{config['api_base_url']}/domicilios",
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
            self.assertTrue("edificio" in item)
            self.assertTrue("estado" in item)
            self.assertTrue("municipio" in item)
            self.assertTrue("calle" in item)
            self.assertTrue("num_ext" in item)
            self.assertTrue("num_int" in item)
            self.assertTrue("colonia" in item)
            self.assertTrue("cp" in item)

    def test_get_domicilio_slt_cj(self):
        """Test GET domicilio clave SLT-CJ"""
        clave = "SLT-CJ"
        response = requests.get(
            url=f"{config['api_base_url']}/domicilios/{clave}",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue("success" in payload)
        self.assertTrue(payload["success"])
        self.assertTrue("message" in payload)
        self.assertTrue("data" in payload)
        self.assertIsInstance(payload["data"], dict)
        data = payload["data"]
        self.assertEqual(data.get("clave"), clave)


if __name__ == "__main__":
    unittest.main()
