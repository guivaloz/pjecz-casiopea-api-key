"""
Unit tests cit oficinas servicios
"""

import unittest

import requests

from tests import config


class TestCitOficinasServicios(unittest.TestCase):
    """Test cit oficinas servicios"""

    def test_get_cit_oficinas_servicios_from_slt_op(self):
        """Test GET cit_oficinas_servicios from oficina_clave SLT-OP"""
        clave = "SLT-OP"
        response = requests.get(
            url=f"{config['api_base_url']}/cit_oficinas_servicios",
            headers={"X-Api-Key": config["api_key"]},
            params={"oficina_clave": clave},
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
            self.assertTrue("cit_servicio_clave" in item)
            self.assertTrue("cit_servicio_descripcion" in item)
            self.assertTrue("oficina_clave" in item)
            self.assertTrue("oficina_descripcion" in item)
            self.assertTrue("oficina_descripcion_corta" in item)
            self.assertEqual(item["oficina_clave"], clave)

    def test_get_cit_oficinas_servicios_from_revexp(self):
        """Test GET cit_oficinas_servicios from servicio_clave REVEXP"""
        clave = "REVEXP"
        response = requests.get(
            url=f"{config['api_base_url']}/cit_oficinas_servicios",
            headers={"X-Api-Key": config["api_key"]},
            params={"cit_servicio_clave": clave},
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
            self.assertTrue("cit_servicio_clave" in item)
            self.assertTrue("cit_servicio_descripcion" in item)
            self.assertTrue("oficina_clave" in item)
            self.assertTrue("oficina_descripcion" in item)
            self.assertTrue("oficina_descripcion_corta" in item)
            self.assertEqual(item["cit_servicio_clave"], clave)


if __name__ == "__main__":
    unittest.main()
