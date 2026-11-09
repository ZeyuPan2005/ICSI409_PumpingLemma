import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from main import demonstration_text, display_demonstration, main
from pumping_lemma import (
    construct_witness,
    generate_decompositions,
    is_in_language,
    pump_string,
    validate_decomposition,
)


class PumpingLemmaTests(unittest.TestCase):
    def test_witness_construction(self):
        for p in (1, 2, 3, 5):
            with self.subTest(p=p):
                self.assertEqual(construct_witness(p), "0" * p + "1" * p)

    def test_language_membership(self):
        for word in ("", "01", "0011", "000111"):
            with self.subTest(word=word):
                self.assertTrue(is_in_language(word))
        for word in ("001", "011", "0101", "1100", "abc"):
            with self.subTest(word=word):
                self.assertFalse(is_in_language(word))

    def test_decomposition_validation(self):
        w = construct_witness(3)
        self.assertTrue(validate_decomposition("", "0", "00111", 3, w))
        self.assertFalse(validate_decomposition("", "", "000111", 3, w))
        self.assertFalse(validate_decomposition("000", "0", "11", 3, w))
        self.assertFalse(validate_decomposition("", "0", "0111", 3, w))

    def test_pumping_down(self):
        self.assertEqual(pump_string("", "0", "00111", 0), "00111")
        self.assertEqual(pump_string("0", "01", "1", 2), "001011")

    def test_every_small_valid_decomposition_fails_when_pumped_down(self):
        for p in range(1, 7):
            w = construct_witness(p)
            decompositions = list(generate_decompositions(p))
            self.assertEqual(len(decompositions), p * (p + 1) // 2)
            for x, y, z in decompositions:
                with self.subTest(p=p, x=x, y=y):
                    self.assertTrue(validate_decomposition(x, y, z, p, w))
                    pumped = pump_string(x, y, z, 0)
                    self.assertFalse(is_in_language(pumped))

    def test_invalid_cli_input(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["0"]), 2)
            self.assertEqual(main(["not-an-integer"]), 2)

        error_output = stderr.getvalue()
        self.assertEqual(error_output.count("Error:"), 2)
        self.assertIn("positive integer", error_output)

    def test_output_contains_general_argument(self):
        output = demonstration_text(3)
        self.assertIn("Assume, for contradiction", output)
        self.assertIn("For every valid decomposition", output)
        self.assertIn("Conclusion: L is NOT regular.", output)

    def test_display_demonstration_uses_call_time_stdout(self):
        output = io.StringIO()
        with redirect_stdout(output):
            display_demonstration(1)

        self.assertIn("Pumping length: p = 1", output.getvalue())


if __name__ == "__main__":
    unittest.main()
