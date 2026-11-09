"""Command-line interface for the Pumping Lemma demonstration."""

import argparse
import sys
from collections.abc import Sequence
from typing import TextIO

from pumping_lemma import (
    construct_witness,
    is_in_language,
    pump_string,
    validate_decomposition,
    validate_pumping_length,
)


def _display_string(value: str) -> str:
    return value if value else "epsilon"


def demonstration_text(p: int) -> str:
    """Build the complete, readable demonstration for p."""
    validate_pumping_length(p)
    w = construct_witness(p)
    x = ""
    y = "0"
    z = "0" * (p - 1) + "1" * p
    pumped = pump_string(x, y, z, 0)
    decomposition_valid = validate_decomposition(x, y, z, p, w)

    lines = [
        "========================================",
        "      PUMPING LEMMA DEMONSTRATION",
        "========================================",
        "",
        "Language: L = {0^n 1^n | n >= 0}",
        f"Pumping length: p = {p}",
        "",
        "[1] Witness Construction",
        f"    w = {_display_string(w)}",
        f"    |w| = {len(w)} = 2 * p",
        f"    |w| >= p: {'PASS' if len(w) >= p else 'FAIL'}",
        f"    w belongs to L: {'YES' if is_in_language(w) else 'NO'}",
        "",
        "[2] Valid Decomposition",
        f"    x = {_display_string(x)}",
        f"    y = {_display_string(y)}",
        f"    z = {_display_string(z)}",
        "",
        f"    x + y + z = w: {'PASS' if x + y + z == w else 'FAIL'}",
        f"    |y| > 0: {'PASS' if len(y) > 0 else 'FAIL'}",
        f"    |xy| <= p: {'PASS' if len(x + y) <= p else 'FAIL'}",
        f"    Decomposition is valid: {'YES' if decomposition_valid else 'NO'}",
        "",
        "[3] Pumping Step",
        "    j = 0",
        f"    xy^0z = {_display_string(pumped)}",
        "",
        "[4] Membership Check",
        f"    Number of zeros: {pumped.count('0')}",
        f"    Number of ones: {pumped.count('1')}",
        f"    Pumped string belongs to L: {'YES' if is_in_language(pumped) else 'NO'}",
        "",
        "[5] General Argument",
        "    For every valid decomposition with |xy| <= p and |y| > 0,",
        "    x = 0^a and y = 0^b for a >= 0 and b >= 1.",
        "    Therefore z = 0^(p-a-b) 1^p.",
        "",
        "    Pumping down with j = 0 gives xy^0z = 0^(p-b) 1^p.",
        "    Since b >= 1, the pumped string has fewer zeros than ones.",
        "    Thus xy^0z is not in L for every valid decomposition.",
        "    This contradicts the Pumping Lemma requirement for regular languages.",
        "",
        "Conclusion: L is NOT regular.",
        "========================================",
    ]
    return "\n".join(lines)


def display_demonstration(p: int, stream: TextIO = sys.stdout) -> None:
    print(demonstration_text(p), file=stream)


def _parse_pumping_length(raw_value: str) -> int:
    try:
        p = int(raw_value)
    except ValueError as exc:
        raise ValueError("The pumping length p must be a positive integer.") from exc
    validate_pumping_length(p)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Demonstrate the Pumping Lemma proof that 0^n1^n is not regular."
    )
    parser.add_argument(
        "p",
        nargs="?",
        help="a positive integer pumping length (prompted for when omitted)",
    )
    args = parser.parse_args(argv)

    try:
        raw_value = args.p
        if raw_value is None:
            raw_value = input("Enter pumping length p (positive integer): ")
        p = _parse_pumping_length(raw_value)
    except (EOFError, KeyboardInterrupt):
        print("Input cancelled.", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    display_demonstration(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
