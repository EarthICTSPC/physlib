# EIS-PHY-KKR-001 — Formal Kramers–Kronig Relations

**Status:** Research/formalization proposal. No theorem is claimed proved by this document.

## 1. Objective

Establish a reusable PhysLib foundation for Kramers–Kronig relations (KKR), independent of Tian's KKA architecture and independent of any one photonic device. The module should express the assumptions under which causality and analyticity relate the real and imaginary parts of a complex frequency response.

KKR is not a “real-number-only” theory. A response is complex-valued; its real and imaginary components are real-valued functions linked by the analytic structure of the response.

## 2. Proposed module boundaries

Proposed Alpha namespace:

- PhyslibAlpha.Optics.KramersKronig.Basic — conventions, complex response functions, real/imaginary parts, domains.
- PhyslibAlpha.Optics.KramersKronig.HilbertTransform — principal-value/Hilbert-transform definitions and hypotheses.
- PhyslibAlpha.Optics.KramersKronig.Causality — causal time-domain response and Fourier/Laplace convention.
- PhyslibAlpha.Optics.KramersKronig.DispersionRelations — theorem connecting real and imaginary parts under explicit hypotheses.
- PhyslibAlpha.Optics.KramersKronig.Examples — analytic causal response examples and numerical reference cases.

Names are provisional and should follow repository conventions after an API-map review.

## 3. Freeze conventions before proving theorems

The sign of the Hilbert-transform relation depends on the Fourier convention and on whether analyticity is stated in the upper or lower half-plane. The first deliverable must explicitly choose and document:

1. Fourier transform sign convention, e.g. exp(-i omega t) or exp(+i omega t).
2. Causal support convention in time.
3. Analytic half-plane for the frequency response.
4. Hilbert-transform sign and principal-value normalization.
5. High-frequency decay/subtraction assumptions.
6. Whether the theorem is stated for ordinary functions, Lp boundary values, or tempered distributions.

No KKR sign should be hard-coded before these choices are fixed and checked against a cited optics convention.

## 4. Mathematical work packages

### KKR-001A — Definitions and conventions

Define a complex response chi:R->C, its real and imaginary parts, the chosen Fourier convention, and the Hilbert transform with principal-value semantics. State domains and integrability assumptions rather than hiding them in notation.

### KKR-001B — Analytic causal example

Formalize a simple stable causal response with an explicitly derived frequency response. Prove that its real and imaginary parts satisfy the selected Hilbert-transform relation. This is a test case for signs, normalization, and endpoint behavior, not the full general theorem.

### KKR-001C — General dispersion theorem

Formalize the boundary-value theorem for a response analytic in the selected half-plane and satisfying sufficient decay/regularity hypotheses. If the general theorem requires substantial complex-analysis or distribution theory not available in the current dependency set, record the missing lemma/interface rather than weakening assumptions silently.

### KKR-001D — Optical susceptibility example

Add a Lorentz-oscillator susceptibility only after the Fourier/sign convention and the general response assumptions are fixed. Separate ideal lossless limits from damped, causal response.

## 5. Connection to the EIS KKA chain

The dependency direction should be:

\[
\text{KKR response theorem}
\longrightarrow
\text{device transfer model}
\longrightarrow
\text{amplitude--phase calibration}
\longrightarrow
\text{KKA field construction}
\longrightarrow
\text{interference and attention claims}.
\]

The KKR theorem constrains a causal complex response. It does not by itself prove that a particular EAM, SOI phase shifter, or modulator–interferometer cascade realizes Tian's S7 mapping. That requires a device model and measured or simulated evidence with a declared provenance.

## 6. Acceptance criteria

- Fourier, causality, analytic-half-plane, and Hilbert-transform sign conventions are explicit.
- The simple causal example compiles and its KKR identity is proved without new axioms or sorry.
- The general theorem states every regularity, decay, and boundary-value hypothesis.
- Numerical checks independently evaluate both components and the Hilbert-transform relation.
- A source-to-requirement ledger distinguishes theorem, analytic example, fitted model, simulation, measurement, and unresolved assumption.
- No device or KKA claim is inferred from KKR alone.

## 7. Deliverables

1. Lean module(s) in PhyslibAlpha/Optics/KramersKronig/.
2. A convention note with primary optics references.
3. Analytic example and tests.
4. A theorem/assumption ledger.
5. A promotion recommendation only after CI, review, and scope checks.
