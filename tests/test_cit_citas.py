"""
Unit tests cit citas
"""

import unittest

import requests

from tests import config


class TestCitCitas(unittest.TestCase):
    """Test cit citas"""

    def test_get_cit_citas(self):
        """Test GET citas"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_citas",
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

    def test_get_mis_citas_by_cit_cliente_id(self):
        """Test GET mis citas by cit_cliente_id"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_citas/mis_citas",
            headers={"X-Api-Key": config["api_key"]},
            params={"cit_cliente_id": config["cit_cliente_id"]},
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
            self.assertEqual(item.get("cit_cliente_id"), config["cit_cliente_id"])
            self.assertEqual(item.get("cit_cliente_curp"), config["curp"])
            self.assertTrue("cit_cliente_nombre" in item)
            self.assertTrue("cit_cliente_email" in item)
            self.assertTrue("cit_servicio_clave" in item)
            self.assertTrue("cit_servicio_descripcion" in item)
            self.assertTrue("oficina_clave" in item)
            self.assertTrue("oficina_descripcion" in item)
            self.assertTrue("inicio" in item)
            self.assertTrue("termino" in item)
            self.assertTrue("notas" in item)

    def test_get_mis_citas_by_curp(self):
        """Test GET mis citas by curp"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_citas/mis_citas",
            headers={"X-Api-Key": config["api_key"]},
            params={"curp": config["curp"]},
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
            self.assertEqual(item.get("cit_cliente_id"), config["cit_cliente_id"])
            self.assertEqual(item.get("cit_cliente_curp"), config["curp"])
            self.assertTrue("cit_cliente_nombre" in item)
            self.assertTrue("cit_cliente_email" in item)
            self.assertTrue("cit_servicio_clave" in item)
            self.assertTrue("cit_servicio_descripcion" in item)
            self.assertTrue("oficina_clave" in item)
            self.assertTrue("oficina_descripcion" in item)
            self.assertTrue("inicio" in item)
            self.assertTrue("termino" in item)
            self.assertTrue("notas" in item)


if __name__ == "__main__":
    unittest.main()
