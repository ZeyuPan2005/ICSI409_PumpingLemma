# Pumping Lemma Demonstration

This project is the optional ICSI 409 bonus implementation for the language

`L = {0^n 1^n | n >= 0}`.

The program accepts a positive pumping length `p`, constructs the witness
`w = 0^p 1^p`, checks a valid decomposition, pumps the middle part down with
`j = 0`, and explains why the result is outside the language.

## Run the program

From this directory, run either an interactive demonstration:

```text
python main.py
```

or provide the pumping length directly:

```text
python main.py 3
```

## Run the tests

```text
python -m unittest discover -s tests -v
```

## Mathematical proof

Assume a pumping length `p >= 1` and choose `w = 0^p 1^p` in `L`. Every valid
decomposition `w = xyz` with `|xy| <= p` and `|y| > 0` has `x = 0^a` and
`y = 0^b`, where `a >= 0`, `b >= 1`, and `a + b <= p`. Pumping down gives

`xy^0z = 0^(p-b) 1^p`.

This string has fewer zeros than ones, so it is not in `L`. The argument covers
every valid decomposition, which contradicts the Pumping Lemma requirement for
regular languages. Therefore `L` is not regular.

The optional decomposition generator enumerates valid decompositions for small
values of `p` as an educational check. The symbolic argument is the proof.

## Scope and limitations

The program demonstrates this one language and does not decide regularity for
arbitrary languages. It uses only the Python standard library and keeps the
core mathematical operations independent from terminal input and output.
