# Propositional Logic Solutions

## 1. Validity and Satisfiability

### a. Smoke implies Fire

The sentence is:

```text
Smoke ⇒ Fire
```

| Smoke | Fire | Smoke ⇒ Fire |
|---|---|---|
| False | False | True |
| False | True | True |
| True | False | False |
| True | True | True |

The sentence is satisfiable because it is true in some models. It is not valid because it is false when Smoke is true and Fire is false. Therefore, it is **neither valid nor unsatisfiable**.

### b. Equivalence Statement

Sentence to analyze:

```text
((Smoke ∧ Heat) ⇒ Fire) ⇔ ((Smoke ⇒ Fire) ∨ (Heat ⇒ Fire))
```

Complete a truth table or use equivalence rules here.

| Smoke | Heat | Fire | (Smoke ∧ Heat) ⇒ Fire | (Smoke ⇒ Fire) ∨ (Heat ⇒ Fire) | Full equivalence |
|---|---|---|---|---|---|
| False | False | False | True | True | True |
| False | False | True | True | True | True |
| False | True | False | True | True | True |
| False | True | True | True | True | True |
| True | False | False | True | True | True |
| True | False | True | True | True | True |
| True | True | False | False | False | True |
| True | True | True | True | True | True |

The final column is true in every possible model. Therefore, the sentence is **valid**. Since every valid sentence is also satisfiable, it is satisfiable as well.

## 2. Models

### a. B or C

Determine the number of models over the vocabulary A, B, C, and D.

There are four propositions, so there are `2^4 = 16` possible models. The sentence `B ∨ C` is false only when both B and C are false. In that case, A and D can each have either value, giving `2^2 = 4` false models. Therefore, the number of models is:

```text
16 - 4 = 12 models
```

### b. The Second Sentence

Determine the number of models for:

```text
(A ⇒ B) ∧ A ∧ ¬B ∧ C ∧ D
```

There are no models. The sentence requires A to be true and B to be false. However, when A is true and B is false, `A ⇒ B` is false. Therefore, the whole conjunction is unsatisfiable and has **0 models**.

## 3. Resolution

### a. Enumeration

Analyze:

```text
[(Food ⇒ Party) ∨ (Drinks ⇒ Party)] ⇒ [(Food ∧ Drinks) ⇒ Party]
```

Let `F` mean Food, `D` mean Drinks, and `P` mean Party. The relevant expressions are:

```text
Food ⇒ Party = ¬F ∨ P
Drinks ⇒ Party = ¬D ∨ P
(Food ∧ Drinks) ⇒ Party = ¬F ∨ ¬D ∨ P
```

The left side becomes `¬F ∨ ¬D ∨ P`, and the right side also becomes `¬F ∨ ¬D ∨ P`. Therefore, the main sentence has the form `X ⇒ X`, which is true for every assignment of F, D, and P. The sentence is **valid**, and therefore it is also satisfiable.

### b. CNF Conversion

Show the conversion of the left-hand and right-hand sides into CNF.

Left-hand side:

```text
(F ⇒ P) ∨ (D ⇒ P)
= (¬F ∨ P) ∨ (¬D ∨ P)
= ¬F ∨ ¬D ∨ P
```

This is already one CNF clause:

```text
(¬F ∨ ¬D ∨ P)
```

Right-hand side:

```text
(F ∧ D) ⇒ P
= ¬(F ∧ D) ∨ P
= (¬F ∨ ¬D) ∨ P
= ¬F ∨ ¬D ∨ P
```

This is the same CNF clause:

```text
(¬F ∨ ¬D ∨ P)
```

### c. Resolution Proof

Provide the resolution proof and explain how it confirms the enumeration result.

To prove validity using resolution, negate the complete implication. Let:

```text
X = (¬F ∨ ¬D ∨ P)
```

The original sentence is `X ⇒ X`. Its negation is:

```text
X ∧ ¬X
```

The CNF clauses are:

```text
C1 = {¬F, ¬D, P}
C2 = {F}
C3 = {D}
C4 = {¬P}
```

Resolve `C1` with `C2`:

```text
{¬F, ¬D, P} and {F} → {¬D, P}
```

Resolve the result with `C3`:

```text
{¬D, P} and {D} → {P}
```

Resolve the result with `C4`:

```text
{P} and {¬P} → {}
```

The empty clause is derived, so the negation is unsatisfiable. Therefore, the original sentence is valid, confirming the enumeration result.
