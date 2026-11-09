# ICSI 409 — Individual Mini-Project: Pumping Lemma Demonstration

## Overview

This project demonstrates the Pumping Lemma argument for

`L = {0^n 1^n | n >= 0}`

and shows that this language is not regular. The command-line program presents
the symbolic proof first, then illustrates the proof with a user-provided
pumping length.

## Mathematical proof

Assume, for contradiction, that `L` is regular. The Pumping Lemma then gives a
pumping length `p >= 1`. Choose the witness

`w = 0^p 1^p`.

The witness belongs to `L`, and `|w| = 2p >= p`.

Consider any valid decomposition `w = xyz` satisfying `|xy| <= p` and
`|y| > 0`. The first `p` symbols of `w` are zeros, so every valid
decomposition has the form

`x = 0^a`, `y = 0^b`, and `z = 0^(p-a-b) 1^p`,

where `a >= 0`, `b >= 1`, and `a + b <= p`. This covers every valid
decomposition, not only the representative split shown by the program.

Choose `j = 0`. Then

`xy^0z = 0^(p-b) 1^p`.

Because `b >= 1`, the pumped string has fewer zeros than ones, so it is not in
`L`. This contradicts the Pumping Lemma requirement that a valid decomposition
remain in the language for every nonnegative pumping value. Therefore,
`L = {0^n 1^n | n >= 0}` is not regular.

## Proof-first output

The program prints four sections in this order:

1. **Proof Setup** states the contradiction assumption, the pumping length, and
   the symbolic witness.
2. **General Proof** handles every valid decomposition and pumps down with
   `j = 0`.
3. **Concrete Demonstration** uses the supplied `p` and the representative
   decomposition `x = epsilon`, `y = 0`, and `z = 0^(p-1) 1^p`.
4. **Conclusion** restates the contradiction and the non-regularity result.

The concrete split illustrates the pumping operation. The symbolic argument in
**General Proof** establishes the result for every valid split.

## Implementation

`pumping_lemma.py` contains the mathematical operations. `main.py` handles
input validation and the proof-first command-line presentation.

| Mathematical concept | Python function | Responsibility |
| --- | --- | --- |
| Witness construction | `construct_witness(p)` | Builds `0^p 1^p`. |
| Language membership | `is_in_language(w)` | Checks the `0^n 1^n` form, including the empty string. |
| Decomposition constraints | `validate_decomposition(...)` | Checks `w = xyz`, `|y| > 0`, and `|xy| <= p`. |
| Pumping | `pump_string(x, y, z, j)` | Constructs `xy^jz`. |
| Finite enumeration | `generate_decompositions(p)` | Generates valid decompositions for testing and study. |

## Usage and testing

Requires Python 3.10 or later.

Run interactively and enter a positive pumping length when prompted:

```text
python main.py
```

Or provide `p` as a command-line argument:

```text
python main.py 3
```

Run the unit tests with:

```text
python -m unittest discover -s tests -v
```

A proof-first execution for `p = 3` includes:

```text
[1] Proof Setup
[2] General Proof
    For every valid decomposition with |xy| <= p and |y| > 0,
[3] Concrete Demonstration
    Representative Decomposition
        xy^0z = 00111
[4] Conclusion
    Therefore, L is NOT regular.
```

The repository includes the actual execution outputs [outputs/p3.txt](outputs/p3.txt)
and [outputs/p5.txt](outputs/p5.txt).

## Scope and limitations

The program demonstrates the Pumping Lemma argument for this specified
language. It does not determine regularity for arbitrary languages. The CLI
prints one representative valid decomposition. `generate_decompositions(p)` is
available for finite enumeration and testing, but it is not a separate CLI
feature. Finite enumeration supports testing and intuition, while the symbolic
argument supplies the proof. Very large pumping lengths can produce long
strings and are outside the intended practical usage.
