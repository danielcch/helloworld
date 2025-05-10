import unittest
import pytest

from app import util


@pytest.mark.unit
class TestUtil(unittest.TestCase):
    def test_convert_to_number_correct_param(self):
        self.assertEqual(4, util.convert_to_number("4"))
        self.assertEqual(0, util.convert_to_number("0"))
        self.assertEqual(0, util.convert_to_number("-0"))
        self.assertEqual(-1, util.convert_to_number("-1"))
        self.assertAlmostEqual(4.0, util.convert_to_number("4.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("0.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("-0.0"), delta=0.0000001)
        self.assertAlmostEqual(-1.0, util.convert_to_number("-1.0"), delta=0.0000001)

    def test_convert_to_number_invalid_type(self):
        self.assertRaises(TypeError, util.convert_to_number, "")
        self.assertRaises(TypeError, util.convert_to_number, "3.h")
        self.assertRaises(TypeError, util.convert_to_number, "s")
        self.assertRaises(TypeError, util.convert_to_number, None)
        self.assertRaises(TypeError, util.convert_to_number, object())
    
    def test_multiply_valid_inputs(self):
        response = self.client.get("/calc/multiply/3/4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "12")

    def test_multiply_invalid_inputs(self):
        response = self.client.get("/calc/multiply/a/2")
        self.assertEqual(response.status_code, 400)
        self.assertIn("TypeError", response.data.decode())

        response = self.client.get("/calc/multiply/3.5.6/2")
        self.assertEqual(response.status_code, 400)
        self.assertIn("TypeError", response.data.decode())

    def test_divide_valid_inputs(self):
        response = self.client.get("/calc/divide/10/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "5.0")

    def test_divide_by_zero(self):
        response = self.client.get("/calc/divide/10/0")
        self.assertEqual(response.status_code, 400)
        self.assertIn("division by zero", response.data.decode().lower())

    def test_divide_invalid_inputs(self):
        response = self.client.get("/calc/divide/3/x")
        self.assertEqual(response.status_code, 400)
        self.assertIn("TypeError", response.data.decode())

        response = self.client.get("/calc/divide/None/2")
        self.assertEqual(response.status_code, 400)
        self.assertIn("TypeError", response.data.decode())

if __name__ == "__main__":  # pragma: no cover
    unittest.main()