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

    def test_get_oficina_cjs_cemasc(self):
        """Test GET for oficina CJS-CEMASC"""
        clave = "CJS-CEMASC"
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
        self.assertEqual(data.get("clave"), "CJS-CEMASC")
        self.assertEqual(data.get("descripcion"), "CENTRO DE MEDIOS ALTERNOS")
        self.assertEqual(data.get("descripcion_corta"), "CEMASC")
        self.assertEqual(data.get("domicilio_clave"), "CJS")
        self.assertEqual(
            data.get("domicilio_completo"),
            "LOS FUNDADORES #7262, MIRASIERRA, SALTILLO, COAHUILA DE ZARAGOZA, C.P. 25016",
        )
        self.assertEqual(data.get("domicilio_edificio"), "CIUDAD JUDICIAL DE SALTILLO")
        self.assertEqual(data.get("es_jurisdiccional"), False)


if __name__ == "__main__":
    unittest.main()
