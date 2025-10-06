"""
Unit tests usuarios
"""

import unittest

import requests

from tests import config


class TestUsuarios(unittest.TestCase):
    """Test usuarios"""

    def test_get_usuarios(self):
        """Test GET usuarios"""
        response = requests.get(
            f"{config['api_base_url']}/usuarios",
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
            self.assertTrue("email" in item)
            self.assertTrue("nombres" in item)
            self.assertTrue("apellido_paterno" in item)
            self.assertTrue("apellido_materno" in item)
            self.assertTrue("puesto" in item)

    def test_get_usuario_no_definido(self):
        """Test GET usuario email no.definido@pjecz.gob.mx"""
        email = "no.definido@pjecz.gob.mx"
        response = requests.get(
            url=f"{config['api_base_url']}/usuarios/{email}",
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
        self.assertEqual(data.get("autoridad_clave"), "OM-DI")
        self.assertEqual(data.get("autoridad_descripcion"), "DIRECCION DE INFORMATICA")
        self.assertEqual(data.get("autoridad_descripcion_corta"), "INFORMATICA")
        self.assertEqual(data.get("distrito_clave"), "ND")
        self.assertEqual(data.get("distrito_nombre"), "NO DEFINIDO")
        self.assertEqual(data.get("distrito_nombre_corto"), "NO DEFINIDO")
        self.assertEqual(data.get("email"), "no.definido@pjecz.gob.mx")
        self.assertEqual(data.get("nombres"), "NO")
        self.assertEqual(data.get("apellido_paterno"), "DEFINIDO")
        self.assertEqual(data.get("apellido_materno"), "")
        self.assertEqual(data.get("puesto"), "NO DEFINIDO")


if __name__ == "__main__":
    unittest.main()
