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


if __name__ == "__main__":
    unittest.main()
