# Optics / Interference — Gaussian Random Features for Complex Fields

**Status:** PhyslibAlpha specification draft. The theorem statements below are the intended scope; the corresponding Gaussian-feature Lean source is not yet present in this branch and must not be described as compiled or proved.

**Source:** Tian, Y. et al., *Photonic Transformer Chip: Interference Is All You Need*, *PhotoniX* 6, 45 (2025), DOI: https://doi.org/10.1186/s43074-025-00182-7. Relevant equations: Supplementary Information 2, S5–S10.

## 1. Scope and place in the EIS programme

This is a narrow mathematical specification for exact Gaussian random-feature identities relevant to Tian et al.'s S5–S6 argument. It is not a formalization of Kramers–Kronig relations (KKR), a photonic device, or the complete Kramers–Kronig attention (KKA) architecture.

The layers must remain distinct:

1. **KKR physics:** under suitable causality, analyticity, and regularity assumptions, real and imaginary parts of a complex response are related by Hilbert transforms.
2. **Device amplitude–phase coupling:** a specific optical transfer response connects device inputs to a complex field. This requires a material/device model and, ultimately, characterization.
3. **KKA computation:** Tian et al. exploit amplitude–phase coupling and optical interference in a computational architecture.
4. **Gaussian random-feature mathematics:** the identities below provide exact mathematical reference kernels relevant to S5–S6.

This draft addresses layer 4 only. It does not establish that a device satisfies KKR, realizes S7, or implements an attention approximation.

## 2. Mathematical setting

Let d be a natural number, q, k, and omega belong to R^d, and let omega have the standard Gaussian distribution N(0,I_d). The real inner product is <.,.>, with squared norm ||x||^2=<x,x>.

### 2.1 S5 — real Gaussian random-feature identity (reference)

Tian et al. state the exponential dot-product identity

\[
e^{\langle q,k\rangle}
=
\mathbb E_\omega\left[
 e^{\langle\omega,q\rangle-\|q\|^2/2}
 e^{\langle\omega,k\rangle-\|k\|^2/2}
\right].
\]

This is the reference identity. In this specification it is a baseline, not the primary contribution.

### 2.2 S6 — complex-bilinear continuation (primary target)

Applying the substitutions q -> i q and k -> -i k to the feature expressions requires the **complex-bilinear extension** of the real quadratic form. In particular,

\[
(iq)\cdot(iq)=-\|q\|^2,
\]

not the Hermitian norm ||iq||^2=||q||^2. Thus the two feature factors have positive quadratic exponents:

\[
\exp\left(i\langle\omega,q\rangle+\frac{\|q\|^2}{2}\right)
\exp\left(-i\langle\omega,k\rangle+\frac{\|k\|^2}{2}\right).
\]

Their Gaussian expectation is

\[
\boxed{
\mathbb E_\omega\left[
 e^{i\langle\omega,q\rangle+\|q\|^2/2}
 e^{-i\langle\omega,k\rangle+\|k\|^2/2}
\right]=e^{\langle q,k\rangle}.
}
\]

This is the primary theorem target and the bilinear S6 identity. A prospective Lean name is gaussian_complex_feature_expectation.

The feature magnitude is e^(||q||^2/2), independent of omega and not uniformly bounded as q varies. The proof should make the Gaussian characteristic-function step and integrability assumptions explicit.

### 2.3 Companion result — a distinct Hermitian feature construction

This is **not** a second interpretation of Tian's S6. It is a separate complex-feature definition using the Hermitian norm:

\[
e^{i\langle\omega,q\rangle-\|q\|^2/2}
e^{-i\langle\omega,k\rangle-\|k\|^2/2}.
\]

Its exact expectation is

\[
\boxed{
\mathbb E_\omega[\cdots]
=e^{\langle q,k\rangle-\|q\|^2-\|k\|^2}.
}
\]

This is a mathematically valid companion kernel with feature magnitudes at most one. A prospective Lean name is gaussian_hermitian_feature_expectation. It must not be attributed to Tian's S6.

### 2.4 Companion result — normalized attention cancellation

For kappa(q,k_i)=e^(<q,k_i>-||q||^2-||k_i||^2), normalization gives

\[
\frac{\kappa(q,k_i)}{\sum_j\kappa(q,k_j)}
=
\frac{e^{\langle q,k_i\rangle-\|k_i\|^2}}
{\sum_j e^{\langle q,k_j\rangle-\|k_j\|^2}}.
\]

The common query factor cancels. This is an algebraic identity, not a Gaussian theorem, and corresponds to a key-norm-penalized SoftMax. Prospective Lean name: hermitian_attention_query_factor_cancels.

## 3. S7–S10: follow-up, not established by this module

### 3.1 S7 scalar amplitude–phase map

For r=|q| with 0<r<1, define

\[
u(r)=\sqrt{-2\ln r},\qquad
\phi_{\rm KKA}(u(r))=\frac{\phi(r)}{u(r)}.
\]

Then

\[
r e^{i\phi(r)}
=e^{-u(r)^2/2}e^{i\phi_{\rm KKA}(u(r))u(r)}
\]

is an algebraic identity under the map. The same construction applies to the key with the appropriate conjugate-phase convention.

The natural open domain for a finite, nonzero mapped amplitude and a defined phase map is 0<r<1. As r->0+, u(r)->+infinity while 1/u(r)->0 for finite original phase. As r->1-, u(r)->0 and the phase-map denominator tends to zero. The endpoints require explicit treatment; r=0 makes the logarithm undefined and r=1 makes the phase map undefined for general nonzero phase.

The scalar identity is distinct from the expanded feature-vector display. The latter has a query-phase sign discrepancy in the source page: the scalar equations use opposite query/key phase signs, while the expanded display appears to use negative signs in both columns. That source-audit issue remains open. The scalar identity does not prove that the mapped feature-product expectation equals S6.

### 3.2 S8–S10 phase–amplitude approximation conditions

S8–S10 state approximate relationships between phase and amplitude, including the forms

\[
\phi(r)\sim r\sqrt{-2\ln r},\qquad
\varphi(r)\sim r\sqrt{-2\ln r}.
\]

These concern joint phase–amplitude behavior, not amplitude distributions alone. The source does not fully specify the normalization and metric semantics of ~. A formal probability statement requires those choices. Figure S5 motivates amplitude-side constructions but does not prove that trained networks maintain the required phase–amplitude relationship across layers, tokens, or workloads.

## 4. Numerical evidence and proof status

Python notebook results are corroborating numerical checks, not Lean proofs and not physical qualification:

- 001B: finite-sample S5 sanity check.
- 001I-A: finite-sample bilinear S6 check; the exact identity is supported analytically by the Gaussian characteristic function.
- 001E: Hermitian companion-kernel numerical check; not Tian S6.
- 001F: Hermitian query-factor cancellation check.
- 001I-C: S7 scalar-field identity and expanded-vector sign discrepancy.
- 001I-D: independent synthetic phases are a negative control for S9/S10; its original varying-pair S6 diagnostic is not a valid fixed-pair expectation estimate.
- 001I-E: proposed Figure S5 experiment; uniform phase assumptions must be labeled as EIS choices unless confirmed by the source.

The Lean implementation must be built against the repository's pinned toolchain and Mathlib manifest before any theorem is described as proved. The source code and CI result, not this specification or a notebook, determine formal proof status.

## 5. Out of scope

- KKR response-function and Hilbert-transform theorems.
- Physical modulator transfer functions, material parameters, detector response, loss, noise, thermal effects, and foundry qualification.
- S7 expanded-vector resolution and S7-to-S6 kernel correspondence.
- S8–S10 distributional semantics and trained-network evidence.
- Finite-sample normalized-ratio error bounds. Such bounds require additional moment, integrability, and denominator-separation assumptions; unbiased numerator and denominator estimates alone do not establish an O(1/m) ratio-bias bound.

## 6. Intended theorem inventory

| Prospective Lean name | Meaning | Status |
|---|---|---|
| gaussian_complex_feature_expectation | Bilinear S6 expectation equals exp(<q,k>) | Specification only |
| gaussian_hermitian_feature_expectation | Separate Hermitian kernel expectation | Specification only |
| hermitian_attention_query_factor_cancels | Algebraic query-factor cancellation | Specification only |

The module should remain in PhyslibAlpha until the implementation compiles, its assumptions and theorem statements are reviewed, and the project promotion criteria are met.
