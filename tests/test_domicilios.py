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

    def test_get_domicilio_cjs(self):
        """Test GET domicilio CJS"""
        clave = "CJS"
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
        self.assertEqual(data.get("clave"), "CJS")
        self.assertEqual(data.get("edificio"), "CIUDAD JUDICIAL DE SALTILLO")
        self.assertEqual(data.get("estado"), "COAHUILA DE ZARAGOZA")
        self.assertEqual(data.get("municipio"), "SALTILLO")
        self.assertEqual(data.get("calle"), "LOS FUNDADORES")
        self.assertEqual(data.get("num_ext"), "7262")
        self.assertEqual(data.get("num_int"), "")
        self.assertEqual(data.get("colonia"), "MIRASIERRA")
        self.assertEqual(data.get("cp"), 25016)
        self.assertEqual(
            data.get("completo"),
            "LOS FUNDADORES #7262, MIRASIERRA, SALTILLO, COAHUILA DE ZARAGOZA, C.P. 25016",
        )


if __name__ == "__main__":
    unittest.main()
