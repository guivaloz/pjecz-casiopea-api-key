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


if __name__ == "__main__":
    unittest.main()
