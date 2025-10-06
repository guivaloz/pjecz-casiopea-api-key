"""
Unit tests autoridades
"""

import unittest

import requests

from tests import config


class TestAutoridades(unittest.TestCase):
    """Test autoridades"""

    def test_get_autoridades(self):
        """Test GET autoridades"""
        response = requests.get(
            url=f"{config['api_base_url']}/autoridades",
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
        self.assertGreater(len(payload["data"]), 0)
        for item in payload["data"]:
            self.assertTrue("clave" in item)
            self.assertTrue("descripcion" in item)
            self.assertTrue("descripcion_corta" in item)
            self.assertTrue("es_jurisdiccional" in item)

    def test_get_autoridad_om_di(self):
        """Test GET autoridad clave OM-DI"""
        clave = "OM-DI"
        response = requests.get(
            url=f"{config['api_base_url']}/autoridades/{clave}",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue("success" in payload)
        self.assertTrue(payload["success"])
        self.assertTrue("message" in payload)
        self.assertTrue("data" in payload)
        self.assertTrue(isinstance(payload["data"], dict))
        data = payload["data"]
        self.assertEqual(data.get("clave"), "OM-DI")
        self.assertEqual(data.get("descripcion"), "DIRECCION DE INFORMATICA")
        self.assertEqual(data.get("descripcion_corta"), "INFORMATICA")
        self.assertEqual(data.get("distrito_clave"), "ND")
        self.assertEqual(data.get("distrito_nombre"), "NO DEFINIDO")
        self.assertEqual(data.get("distrito_nombre_corto"), "NO DEFINIDO")
        self.assertEqual(data.get("materia_clave"), "ND")
        self.assertEqual(data.get("materia_nombre"), "NO DEFINIDO")
        self.assertEqual(data.get("es_jurisdiccional"), False)


if __name__ == "__main__":
    unittest.main()
