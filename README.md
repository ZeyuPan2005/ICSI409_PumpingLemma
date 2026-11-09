# ICSI 409 Individual Bonus Mini Project

## Overview

This project is the ICSI 409 Individual Bonus Mini-Project for Option 2, a
Pumping Lemma demonstration. It studies

`L = {0^n 1^n | n >= 0}`

and presents the contradiction argument showing that this language is not
regular. The program is intentionally small and uses only the Python standard
library.

## Mathematical background and proof

Assume, for contradiction, that `L` is regular. The Pumping Lemma then gives a
pumping length `p >= 1`. Choose the witness

`w = 0^p 1^p`.

The witness belongs to `L`, and `|w| = 2p >= p`.

Now consider any valid decomposition `w = xyz` satisfying `|xy| <= p` and
`|y| > 0`. The first `p` symbols of `w` are all zeros, so every such
decomposition has the form

`x = 0^a`, `y = 0^b`, and `z = 0^(p-a-b) 1^p`,

where `a >= 0`, `b >= 1`, and `a + b <= p`. This describes every valid
decomposition, not only the representative decomposition printed by the
program.

Choose `j = 0`. Pumping down gives

`xy^0z = 0^(p-b) 1^p`.

Because `b >= 1`, the pumped string has fewer zeros than ones, so it is not in
`L`. This contradicts the Pumping Lemma requirement that a valid decomposition
remain in the language for every nonnegative pumping value. Therefore,
`L = {0^n 1^n | n >= 0}` is not regular.

## Implementation

The implementation separates the mathematical operations from the command-line
presentation.

| Mathematical concept | Python function | Responsibility |
| --- | --- | --- |
| Witness construction | `construct_witness(p)` | Builds `0^p 1^p`. |
| Language membership | `is_in_language(w)` | Checks the `0^n 1^n` form, including the empty string. |
| Decomposition constraints | `validate_decomposition(...)` | Checks `w = xyz`, `|y| > 0`, and `|xy| <= p`. |
| Pumping | `pump_string(x, y, z, j)` | Constructs `xy^jz`. |
| Finite enumeration | `generate_decompositions(p)` | Generates every valid decomposition for testing and study. |

`pumping_lemma.py` contains these mathematical operations. `main.py` handles
input validation and presents one representative decomposition followed by the
general proof.

## Usage and testing

Python 3.10 or newer is recommended.

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

A representative execution for `p = 3` includes:

```text
w = 000111
|w| = 6 = 2 * p
xy^0z = 00111
Pumped string belongs to L: NO
Conclusion: L is NOT regular.
```

The repository also includes the execution outputs [outputs/p3.txt](outputs/p3.txt)
and [outputs/p5.txt](outputs/p5.txt).

## Scope and limitations

The program demonstrates the Pumping Lemma argument for this specified
language. It does not determine regularity for arbitrary languages. The CLI
prints one representative valid decomposition. `generate_decompositions(p)` is
available for finite enumeration and testing, but it is not a separate CLI
feature. Finite enumeration supports testing and intuition, while the symbolic
argument supplies the proof. Very large pumping lengths can produce long
strings and are outside the intended practical usage.

No separate formal report is required for this bonus project.
