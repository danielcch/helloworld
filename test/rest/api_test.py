import http.client
import os
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

BASE_URL = os.getenv("BASE_URL_ENV", "http://localhost:5000")
BASE_URL_MOCK = os.getenv("BASE_URL_MOCK_ENV", "http://localhost:9090")

DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )
    
    def test_api_multiply_valid(self):
        url = f"{BASE_URL}/calc/multiply/6/7"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "42", "ERROR MULTIPLY"
        )

    def test_api_multiply_invalid(self):
        url = f"{BASE_URL}/calc/multiply/a/5"
        with self.assertRaises(HTTPError) as context:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(context.exception.code, http.client.BAD_REQUEST)

    def test_api_divide_valid(self):
        url = f"{BASE_URL}/calc/divide/20/4"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "5.0", "ERROR DIVIDE"
        )

    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/10/0"
        with self.assertRaises(HTTPError) as context:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(context.exception.code, http.client.BAD_REQUEST)

    def test_api_divide_invalid(self):
        url = f"{BASE_URL}/calc/divide/2/x"
        with self.assertRaises(HTTPError) as context:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(context.exception.code, http.client.BAD_REQUEST)

    

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
