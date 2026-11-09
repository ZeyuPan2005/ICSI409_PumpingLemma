"""Core operations for the Pumping Lemma demonstration."""

from collections.abc import Iterator


def validate_pumping_length(p: int) -> None:
    """Reject values that cannot serve as a positive pumping length."""
    if isinstance(p, bool) or not isinstance(p, int) or p <= 0:
        raise ValueError("The pumping length p must be a positive integer.")


def construct_witness(p: int) -> str:
    """Construct w = 0^p 1^p for a positive pumping length."""
    validate_pumping_length(p)
    return "0" * p + "1" * p


def is_in_language(w: str) -> bool:
    """Return whether w belongs to L = {0^n 1^n | n >= 0}."""
    if not isinstance(w, str) or any(symbol not in "01" for symbol in w):
        return False

    zero_count = w.count("0")
    one_count = w.count("1")
    return zero_count == one_count and w == "0" * zero_count + "1" * one_count


def validate_decomposition(x: str, y: str, z: str, p: int, w: str) -> bool:
    """Check the decomposition constraints required by the Pumping Lemma."""
    validate_pumping_length(p)
    return (
        all(isinstance(part, str) for part in (x, y, z, w))
        and x + y + z == w
        and len(y) > 0
        and len(x + y) <= p
    )


def pump_string(x: str, y: str, z: str, j: int) -> str:
    """Return xy^jz for a nonnegative pumping value j."""
    if isinstance(j, bool) or not isinstance(j, int) or j < 0:
        raise ValueError("The pumping value j must be a nonnegative integer.")
    return x + y * j + z


def generate_decompositions(p: int) -> Iterator[tuple[str, str, str]]:
    """Yield every valid decomposition of 0^p 1^p under |xy| <= p.

    Since the first p symbols of the witness are zeros, every valid y consists
    of one or more zeros. The generator avoids storing all decompositions.
    """
    w = construct_witness(p)
    for x_length in range(p + 1):
        for y_length in range(1, p - x_length + 1):
            x = w[:x_length]
            y = w[x_length : x_length + y_length]
            z = w[x_length + y_length :]
            yield x, y, z
