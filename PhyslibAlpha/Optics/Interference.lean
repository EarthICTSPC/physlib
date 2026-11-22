/- 
Copyright (c) 2026 Earth ICT, SPC. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Earth ICT, SPC
-/
module
public import Mathlib.Analysis.InnerProductSpace.Basic
public import Mathlib.Analysis.Complex.Norm
public import Mathlib.Basic.Complex.Basic

/-!
# Optics.Interference

Basic identities for the interference of two complex optical field amplitudes.

The results in this file are mathematical statements about complex amplitudes.
They do not assume a particular waveguide, coupler, modulator, or detector
implementation.
-/

@[expose] public section

namespace Optics

/-- The real cross-term between two complex field amplitudes.

It is the real inner product `⟪b, a⟫_ℝ`, equivalently
`Re (a * conj b)`. -/
def opticalCrossTerm (a b : ℂ) : ℝ :=
  ⟪b, a⟫_ℝ

/-- The squared magnitude of a superposition of two complex fields equals
the sum of their individual squared magnitudes plus twice the optical
cross-term. -/
theorem normSq_add_eq_normSq_add_normSq_add_two_mul_crossTerm
    (a b : ℂ) :
    Complex.normSq (a + b) =
      Complex.normSq a + Complex.normSq b +
        2 * opticalCrossTerm a b := by
  rw [Complex.normSq_add]
  rfl

/-- The optical cross-term is symmetric in its two field amplitudes. -/
theorem opticalCrossTerm_comm (a b : ℂ) :
    opticalCrossTerm a b = opticalCrossTerm b a := by
  unfold opticalCrossTerm
  exact real_inner_comm a b

/-- The magnitude of the optical cross-term is bounded by the product
of the field norms. -/
theorem abs_opticalCrossTerm_le_norm_mul_norm (a b : ℂ) :
    |opticalCrossTerm a b| ≤ ‖a‖ * ‖b‖ := by
  unfold opticalCrossTerm
  simpa [mul_comm] using (abs_real_inner_le_norm b a)

end Optics
