"""
Unit tests cit clientes
"""

import unittest

import requests

from tests import config


class TestCitClientes(unittest.TestCase):
    """Test cit clientes"""

    def test_get_cit_clientes(self):
        """Test GET clientes"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_clientes",
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

    def test_perfil_by_cit_cliente_id(self):
        """Test perfil by cit_cliente_id"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_clientes/perfil",
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
        self.assertTrue(isinstance(payload["data"], dict))
        data = payload["data"]
        self.assertEqual(data.get("id"), config["cit_cliente_id"])
        self.assertEqual(data.get("curp"), config["curp"])
        self.assertTrue("nombres" in data)
        self.assertTrue("apellido_primero" in data)
        self.assertTrue("apellido_segundo" in data)
        self.assertTrue("telefono" in data)
        self.assertTrue("email" in data)

    def test_detalle_by_curp(self):
        """Test detalle by curp"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_clientes/perfil",
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
        self.assertTrue(isinstance(payload["data"], dict))
        data = payload["data"]
        self.assertEqual(data.get("id"), config["cit_cliente_id"])
        self.assertEqual(data.get("curp"), config["curp"])
        self.assertTrue("nombres" in data)
        self.assertTrue("apellido_primero" in data)
        self.assertTrue("apellido_segundo" in data)
        self.assertTrue("telefono" in data)
        self.assertTrue("email" in data)


if __name__ == "__main__":
    unittest.main()
