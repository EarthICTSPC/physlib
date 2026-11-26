# EIS-PHY-LOWERING-001 — Multi-Backend Lowering Architecture

**Status:** Architecture proposal. This is an EIS design principle, not an implemented compiler.

## 1. Objective

Enable rapid adoption of first-fuel, energy-efficient Tian KKA computing by allowing one formally governed physical/computational specification to target multiple implementation ecosystems. PhysLib is the semantic and mathematical authority; it is not a single-backend compiler and does not require every implementation to use the same EDA stack.

The target is not “one Lean proof directly emits every file.” The target is a chain of typed, versioned intermediate representations and backend-specific lowering passes, each with explicit contracts and evidence.

## 2. Layered authority

1. **PhysLib mathematical authority:** definitions, assumptions, theorems, invariants, and accepted transformations.
2. **EIS reference specification:** versioned machine-readable contracts for wavelength, complex-field conventions, amplitude/phase maps, topology, timing, energy boundaries, tolerances, and acceptance criteria.
3. **Canonical intermediate representations (IRs):** separate but linked semantic objects for device, photonic circuit, electrical/control, timing, and physical layout.
4. **Backend lowerers:** translate only the IR subsets they support; report unsupported features rather than silently approximating them.
5. **Evidence adapters:** return tool versions, PDK versions, inputs, outputs, solver settings, hashes, warnings, measurements, and acceptance results to the evidence ledger.

## 3. Candidate lowering paths

| Target ecosystem | Lowered artifact | Main evidence |
|---|---|---|
| PhotonForge / FlexCompute | Photonic circuit and device models | Circuit response, S-matrices, time-domain behavior, solver provenance |
| Tidy3D | Electromagnetic geometry and simulation setup | Mesh/boundary/material settings, convergence, field and S-parameter data |
| gdsfactory / SiEPIC / KLayout | PDK-aware layout and OASIS/GDS | DRC/LVS, layer map, geometry, port connectivity, export hashes |
| Foundry PDK flows (e.g. TSMC, GlobalFoundries) | PDK-specific cells, constraints, and handoff data | PDK revision, rule checks, foundry acceptance, process assumptions |
| Electrical/control EDA | Drivers, detectors, timing and control interfaces | Electrical loading, timing, power, parasitics, interface verification |
| Software/reference execution | Numerical reference and test vectors | Deterministic vectors, tolerances, numerical error and provenance |

These are candidate adapters, not assertions that each tool already supports every required feature or that every path is currently available to EIS.

## 4. The contract-preserving lowering rule

A backend may refine or implement a contract, but it may not silently weaken it. Each lowering must carry:

- source specification ID and version;
- source theorem/definition references;
- backend and tool version;
- PDK/process and model versions where applicable;
- units, coordinate frames, wavelength/frequency conventions;
- preserved assumptions and discharged obligations;
- approximations introduced, with explicit error/tolerance bounds;
- unsupported obligations and unresolved fields;
- artifact hashes and reproducibility metadata.

A lowering is accepted only when the backend-specific checks pass and the returned evidence is mapped back to the source contract. “Generated successfully” is not the same as “physically qualified.”

## 5. Typed IR strategy

Do not force all domains into one untyped JSON object. Use a small family of schema-versioned IRs with explicit links:

- PhysicalResponseIR: complex response, causality assumptions, frequency convention, amplitude/phase behavior.
- PhotonicDeviceIR: device ports, transfer functions, materials, geometry parameters, operating envelope.
- PhotonicNetworkIR: components, connectivity, complex fields, phase references, interference operations.
- ElectroThermalTimingIR: drivers, loads, parasitics, thermal paths, control timing, energy accounting.
- LayoutIR: PDK layers, cells, ports, constraints, geometry and export semantics.
- EvidenceIR: provenance, tool runs, results, tolerances, test outcomes, review status.

A backend declares which IR versions and fields it supports. Lossy or partial lowering must be visible in a machine-readable report.

## 6. First-fuel evaluation contract

The objective metric is energy per accepted useful transformation, with quality, latency, throughput, utilization, and lifecycle/system boundaries reported alongside it. A backend cannot claim an energy improvement by omitting driver, detector, conversion, control, cooling, or idle energy outside the declared measurement boundary.

Compare candidate paths against a matched electronic baseline and report measured, simulated, fitted, assumed, and projected quantities separately.

## 7. Adoption sequence

1. Freeze the KKR/KKA mathematical and field conventions.
2. Publish the minimal reference contract and deterministic test vectors.
3. Implement one end-to-end reference lowering path (Lean contract → Python adapter → PhotonForge/Tidy3D evidence).
4. Add layout and OASIS lowering through supported PDK-aware exporters.
5. Add foundry-specific and electrical/control adapters independently.
6. Compare backends on contract preservation, implementation cost, energy per accepted transformation, latency, and reproducibility.

The first backend is a proving path, not a permanent architectural lock-in.

## 8. Acceptance criteria

- One source contract can produce multiple backend-specific artifacts.
- Every backend declares supported/unsupported fields and transformations.
- No silent loss of assumptions, units, phase references, or error bounds.
- Each artifact has provenance and a reproducible evidence package.
- Lean remains the authority for formal claims; tool outputs remain evidence, not proofs of unrelated claims.
- Backend comparisons use the same workloads and energy boundary.
