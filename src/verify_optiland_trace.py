from optiland import optic


lens = optic.Optic(name="Environment smoke-test singlet")
lens.surfaces.add(index=0, radius=float("inf"), thickness=float("inf"))
lens.surfaces.add(
    index=1,
    radius=50.0,
    thickness=5.0,
    material="N-BK7",
    is_stop=True,
)
lens.surfaces.add(index=2, radius=-50.0, thickness=45.0)
lens.surfaces.add(index=3)
lens.set_aperture(aperture_type="EPD", value=10.0)
lens.fields.set_type("angle")
lens.fields.add(y=0.0)
lens.wavelengths.add(value=0.5876, is_primary=True)

rays = lens.trace(
    Hx=0,
    Hy=0,
    wavelength=0.5876,
    num_rays=16,
    distribution="uniform",
)

if len(rays.x) == 0:
    raise RuntimeError("Optiland returned no rays.")

print(f"Optiland trace: OK ({len(rays.x)} rays)")
