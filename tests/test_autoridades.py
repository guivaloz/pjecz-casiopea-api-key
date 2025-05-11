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
        for item in payload["data"]:
            self.assertTrue("clave" in item)
            self.assertTrue("descripcion" in item)
            self.assertTrue("descripcion_corta" in item)
            self.assertTrue("es_jurisdiccional" in item)


    def test_get_autoridades_by_distrito_clave(self):
        """Test GET autoridades by distrito_clave"""
        response = requests.get(
            url=f"{config['api_base_url']}/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"distrito_clave": "ND"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue("success" in payload)
        self.assertTrue(payload["success"])
        self.assertTrue("message" in payload)
        self.assertTrue("data" in payload)
        self.assertTrue(isinstance(payload["data"], list))
        for item in payload["data"]:
            self.assertEqual(item["distrito_clave"], "ND")
            self.assertTrue("clave" in item)
            self.assertTrue("descripcion" in item)
            self.assertTrue("descripcion_corta" in item)
            self.assertTrue("es_jurisdiccional" in item)

if __name__ == "__main__":
    unittest.main()
