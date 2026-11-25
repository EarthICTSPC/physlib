# EIS-LOWER-001A — Canonical PhotonicNetworkIR Contract

**Status:** Frozen candidate v0.1.0 for review. This is a normative interface proposal; it is not yet a backend implementation or a physical qualification.

## 1. Purpose and boundary

Define one backend-neutral representation of photonic computational intent that independent lowerers can consume without changing its meaning. Version 0.1.0 is deliberately limited to coherent complex-field networks and deterministic two-field interference. It establishes the semantic boundary before any PhotonForge, Tidy3D, layout, foundry, or electrical adapter is written.

The IR describes *what is intended*, not how a particular tool implements it. Backend-specific geometry, mesh, solver settings, PDK layers, device compact models, and file formats do not belong in the canonical IR.

## 2. Normative principles

1. **Backend neutrality:** no vendor, simulator, foundry, layout tool, or file-format identifiers are required to interpret the core semantics.
2. **Explicit complex convention:** fields are represented by real and imaginary components; the time-harmonic sign convention and phase-reference identity are declared, never inferred.
3. **Explicit units:** every dimensional quantity carries a unit. Version 0.1.0 test vectors use dimensionless normalized field amplitudes and dimensionless intensity.
4. **No implicit normalization:** intensity means squared field magnitude. Detector responsivity, optical power calibration, photon flux, and electrical current are different quantities and are out of scope unless explicitly modeled by a later IR extension.
5. **No implicit detector model:** the identity |A+B|² is an ideal coherent-field intensity relation, not a balanced-photodetector output claim.
6. **No silent loss:** a lowerer must report unsupported semantics, approximations, tolerances, and discharged or outstanding obligations.
7. **Stable provenance:** every IR instance carries an ID, semantic version, source-contract references, and content digest in its evidence record.

## 3. Version 0.1.0 semantic model

A PhotonicNetworkIR v0.1.0 contains:

- `schema_version`: exact IR schema version.
- `network_id`: stable identifier for the network instance.
- `conventions`: field representation, phasor convention, phase-reference ID, and unit policy.
- `nodes`: uniquely identified components or ports.
- `connections`: directed connections between compatible ports.
- `operations`: explicitly typed mathematical operations and their operand references.
- `assumptions`: machine-readable declarations required to interpret the network.
- `provenance`: source specification identifiers and version references.

The v0.1.0 core node kinds are `field_source`, `phase_shifter`, `amplitude_phase_map`, `interferometer`, and `ideal_intensity_observation`. These are semantic kinds, not prescriptions for physical cells. A node may carry symbolic parameters or concrete values, but the representation must distinguish them.

The canonical complex scalar is `{ "re": number, "im": number }`. The canonical intensity is a nonnegative real scalar. The canonical field is a complex amplitude, not optical power.

## 4. Phase and field conventions

A network must declare:

- the time-harmonic convention (for example, `exp(+i omega t)` or `exp(-i omega t)`);
- the phase-reference identifier shared by fields that interfere;
- whether each field is absolute or relative to that reference;
- the units or normalization of field amplitude;
- the wavelength or frequency and its unit when the model is wavelength/frequency-specific.

Fields with incompatible or undeclared phase references MUST NOT be coherently combined by a conforming lowerer. A backend may support a conversion only when the phase transformation is explicit and recorded.

This IR does not prescribe a global sign convention for all future device models. It requires the convention to be explicit and stable within each network.

## 5. Interference operation

For complex field amplitudes A and B expressed in the same declared reference frame:

```text
I(A,B) = |A + B|^2
       = |A|^2 + |B|^2 + 2 Re(A * conjugate(B))
```

The cross term is `2 * Re(A * conjugate(B))`. The ideal intensity operation is deterministic and does not include loss, detector gain, shot noise, thermal noise, saturation, or electrical conversion.

Equivalent implementations may use complex arithmetic, real-imaginary arithmetic, or a backend-native operation, but must pass the same reference vectors within the declared numerical tolerance.

## 6. Deterministic reference vectors

The companion file `test-vectors/interference-v1.json` is normative for v0.1.0. It defines dimensionless complex fields and expected ideal intensities and cross terms. Values are chosen to cover constructive, destructive, quadrature, unequal-amplitude, and zero-field cases.

A conforming evaluator must:
- reproduce each expected intensity and cross term;
- preserve the declared operand order and conjugation semantics;
- report absolute and relative error;
- report the arithmetic precision and implementation version.

For exact simple values, the expected results are exact mathematical values. Floating-point implementations use a declared tolerance; they must not rewrite the expected values to fit a backend.

## 7. Conformance and lowering report

Every lowerer must emit a conformance report containing:

- source IR schema version and network ID;
- source content digest;
- lowerer name, version, and configuration digest;
- supported and unsupported node/operation kinds;
- transformations performed;
- approximations and numerical error bounds;
- preserved, discharged, and outstanding assumptions;
- generated artifact identifiers and digests;
- test-vector results and tolerances.

A lowerer that cannot preserve a required semantic MUST fail closed or return an explicit partial-lowering status. It MUST NOT label a partial result conformant.

## 8. Versioning and extension policy

- Patch: editorial clarifications that do not alter semantics.
- Minor: backward-compatible optional fields or new node/operation kinds.
- Major: changes to field meaning, phase/conjugation semantics, units, required fields, or existing operation behavior.

Unknown required semantics MUST be rejected. Unknown optional metadata may be retained and ignored. A backend must declare the highest schema version and feature set it supports.

## 9. Explicit exclusions

Version 0.1.0 does not define:
- a foundry-neutral physical model for any specific modulator or coupler;
- KKR proof obligations or a material dispersion model;
- balanced-detector subtraction or photodetector responsivity;
- electro-optic drive, electrical loading, thermal dynamics, or energy accounting;
- layout geometry, DRC/LVS, packaging, or OASIS/GDS export;
- stochastic noise models or finite-sample attention error;
- a claim that KKA implements exact normalized SoftMax.

These are linked future contracts, not implicit properties of this IR.

## 10. Acceptance gate for 001A

001A is complete when:
1. this semantic contract and the JSON Schema validate the same v0.1.0 model;
2. the deterministic reference vectors are consumed by an independent reference evaluator;
3. at least two independent readers can parse the same IR without changing its semantics (they may initially be simple validators, not EDA integrations);
4. conformance reporting exposes unsupported features and approximations;
5. the contract is reviewed and frozen before backend-specific lowering work begins.

**Freeze means semantic stability for v0.1.0, not a claim that the schema is complete for all photonic computing.**
