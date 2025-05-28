"""
Unit tests cit dias inhábiles
"""

import unittest

import requests

from tests import config


class TestCitDiasInhabiles(unittest.TestCase):
    """Test cit dias inhábiles"""

    def test_get_cit_dias_inhabiles(self):
        """Test GET cit dias inhábiles"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_dias_inhabiles",
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


if __name__ == "__main__":
    unittest.main()
