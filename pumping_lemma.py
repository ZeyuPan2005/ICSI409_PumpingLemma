"""Core operations for the Pumping Lemma demonstration."""

from collections.abc import Iterator


def validate_pumping_length(p: int) -> None:
    """Reject values that cannot serve as a positive pumping length."""
    if isinstance(p, bool) or not isinstance(p, int) or p <= 0:
        raise ValueError("The pumping length p must be a positive integer.")


def construct_witness(p: int) -> str:
    """Construct the Pumping Lemma witness w = 0^p 1^p."""
    validate_pumping_length(p)
    return "0" * p + "1" * p


def is_in_language(w: str) -> bool:
    """Return whether w belongs to L = {0^n 1^n | n >= 0}.

    Equal numbers of zeros and ones are necessary but not sufficient. The
    zeros must also occur before all of the ones, so the string must match the
    form 0^n 1^n.
    """
    if not isinstance(w, str) or any(symbol not in "01" for symbol in w):
        return False

    zero_count = w.count("0")
    one_count = w.count("1")
    # The canonical-form check enforces the required order of the symbols.
    return zero_count == one_count and w == "0" * zero_count + "1" * one_count


def validate_decomposition(x: str, y: str, z: str, p: int, w: str) -> bool:
    """Check w = xyz and the Pumping Lemma constraints for this witness.

    The provided decomposition must reconstruct w, have a nonempty y, and
    satisfy |xy| <= p.
    """
    validate_pumping_length(p)
    return (
        all(isinstance(part, str) for part in (x, y, z, w))
        and x + y + z == w
        and len(y) > 0
        and len(x + y) <= p
    )


def pump_string(x: str, y: str, z: str, j: int) -> str:
    """Return xy^jz by repeating y exactly j times."""
    if isinstance(j, bool) or not isinstance(j, int) or j < 0:
        raise ValueError("The pumping value j must be a nonnegative integer.")
    return x + y * j + z


def generate_decompositions(p: int) -> Iterator[tuple[str, str, str]]:
    """Yield every valid decomposition of 0^p 1^p under |xy| <= p.

    The first p symbols of w are zeros, so x and the nonempty y can be chosen
    by their lengths entirely within that prefix. The outer loop chooses the
    length of x. For each x, the inner loop chooses a positive length for y
    without allowing |xy| to exceed p. z is the remaining suffix of w.
    """
    w = construct_witness(p)
    # Both x and y stay within the first p zeros because |xy| <= p.
    for x_length in range(p + 1):
        # Starting at one enforces |y| > 0; the upper bound enforces |xy| <= p.
        for y_length in range(1, p - x_length + 1):
            x = w[:x_length]
            y = w[x_length : x_length + y_length]
            z = w[x_length + y_length :]
            yield x, y, z
