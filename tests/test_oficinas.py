"""
Unit tests oficinas
"""

import unittest

import requests

from tests import config


class TestOficinas(unittest.TestCase):
    """Test oficinas"""

    def test_get_oficinas(self):
        """Test GET oficinas"""
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
            self.assertTrue("clave" in item)
            self.assertTrue("descripcion" in item)
            self.assertTrue("descripcion_corta" in item)
            self.assertTrue("domicilio_clave" in item)
            self.assertTrue("domicilio_completo" in item)
            self.assertTrue("domicilio_edificio" in item)
            self.assertTrue("es_jurisdiccional" in item)

    def test_get_oficinas_from_slt_cj(self):
        """Test GET oficinas from domicilio_clave SLT-CJ"""
        clave = "SLT-CJ"
        response = requests.get(
            url=f"{config['api_base_url']}/oficinas",
            headers={"X-Api-Key": config["api_key"]},
            params={"domicilio_clave": clave},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue("success" in payload)
        self.assertTrue(payload["success"])
        self.assertTrue("message" in payload)
        self.assertTrue("data" in payload)
        self.assertTrue(isinstance(payload["data"], list))
        self.assertGreater(len(payload["data"]), 0)
        for item in payload["data"]:
            self.assertTrue("clave" in item)
            self.assertTrue("descripcion" in item)
            self.assertTrue("descripcion_corta" in item)
            self.assertTrue("domicilio_clave" in item)
            self.assertTrue("domicilio_completo" in item)
            self.assertTrue("domicilio_edificio" in item)
            self.assertTrue("es_jurisdiccional" in item)

    def test_get_oficina_slt_op(self):
        """Test GET oficina clave SLT-OP"""
        clave = "SLT-OP"
        response = requests.get(
            url=f"{config['api_base_url']}/oficinas/{clave}",
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
