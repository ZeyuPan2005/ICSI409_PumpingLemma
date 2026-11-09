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
    """Build a proof-first demonstration for a concrete value of p.

    The symbolic proof comes before one representative numerical example so
    the example illustrates the argument without standing in for it.
    """
    validate_pumping_length(p)
    w = construct_witness(p)

    # This split is one concrete illustration. The symbolic proof covers every
    # valid decomposition, so this choice is not the proof by itself.
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
        "[1] Proof Setup",
        "    Language: L = {0^n 1^n | n >= 0}",
        "    Assume, for contradiction, that L is regular.",
        "    The Pumping Lemma then guarantees a pumping length p >= 1.",
        "    Choose the symbolic witness w = 0^p 1^p.",
        "    w belongs to L and |w| = 2p >= p.",
        "",
        "[2] General Proof",
        "    Consider any valid decomposition w = xyz with:",
        "        |xy| <= p and |y| > 0.",
        "    The first p symbols of w are zeros, so:",
        "        x = 0^a",
        "        y = 0^b",
        "        z = 0^(p-a-b) 1^p",
        "    where a >= 0, b >= 1, and a + b <= p.",
        "    This describes every valid decomposition, not just one example.",
        "",
        "    Choose j = 0.",
        "    xy^0z = 0^(p-b) 1^p.",
        "    Since b >= 1, this string has fewer zeros than ones.",
        "    Therefore xy^0z is not in L for every valid decomposition.",
        "",
        "[3] Concrete Demonstration",
        f"    This illustration uses the supplied p = {p}.",
        "",
        "    Witness",
        f"        w = {_display_string(w)}",
        f"        |w| = {len(w)} = 2 * p",
        f"        |w| >= p: {'PASS' if len(w) >= p else 'FAIL'}",
        f"        w belongs to L: {'YES' if is_in_language(w) else 'NO'}",
        "",
        "    Representative Decomposition",
        "        This split illustrates the pumping operation only.",
        f"        x = {_display_string(x)}",
        f"        y = {_display_string(y)}",
        f"        z = {_display_string(z)}",
        "",
        f"        x + y + z = w: {'PASS' if x + y + z == w else 'FAIL'}",
        f"        |y| > 0: {'PASS' if len(y) > 0 else 'FAIL'}",
        f"        |xy| <= p: {'PASS' if len(x + y) <= p else 'FAIL'}",
        f"        Decomposition is valid: {'YES' if decomposition_valid else 'NO'}",
        "",
        "    Pumping Step",
        "        j = 0",
        f"        xy^0z = {_display_string(pumped)}",
        "",
        "    Membership Check",
        f"        Number of zeros: {pumped.count('0')}",
        f"        Number of ones: {pumped.count('1')}",
        f"        Pumped string belongs to L: {'YES' if is_in_language(pumped) else 'NO'}",
        "",
        "[4] Conclusion",
        "    Every valid decomposition fails to remain in L when j = 0.",
        "    This contradicts the Pumping Lemma under the assumption that L is regular.",
        "    Therefore, L is NOT regular.",
        "========================================",
    ]
    return "\n".join(lines)


def display_demonstration(p: int, stream: TextIO | None = None) -> None:
    """Print the demonstration, resolving stdout at call time by default."""
    if stream is None:
        stream = sys.stdout
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
