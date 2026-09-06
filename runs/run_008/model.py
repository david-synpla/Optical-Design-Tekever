"""B05 co-designed Cassegrain/corrector screen; fresh requirements-derived seed.

The mechanical aperture sizes and merit weights are benchmark assumptions.
All old runs are read-only. Run using the configured WSL scientific Python.
"""
from pathlib import Path
import sys, json, time, shutil, hashlib, csv
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import least_squares, minimize_scalar
from scipy.ndimage import map_coordinates
from optiland import optic
from optiland.physical_apertures import RadialAperture
from optiland.psf import ScalarFFTPSF
import optiland, scipy, yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
R=yaml.safe_load((ROOT/'requirements/eo_requirements.yaml').read_text())['source_explicit_requirements']
F=R['pixel_pitch_um'][0]*1000/R['instantaneous_fov_urad_per_pixel']; D=F/R['f_number']
W,H=np.array(R['array_px'])*R['pixel_pitch_um'][0]/1000
ANG=np.degrees(np.arctan(np.hypot(W,H)/(2*F)))
HX=np.degrees(np.arctan(W/(2*F)))/ANG; HY=np.degrees(np.arctan(H/(2*F)))/ANG
WAVES=[.43,.50,.55,.65,.725,.80]; FREQ=np.array([50,100,150,1000/(2*R['pixel_pitch_um'][0])])
FIELDS=[(a*HX,b*HY) for a in [-1,0,1] for b in [-1,0,1]]
# Fixed mechanical radii, NOT customer requirements; held fixed throughout solve.
AP={'entrance_outer':D/2,'obstruction':35.5,'primary_outer':66.5,'hole':21.5,'secondary':35.5,'lens1':17.5,'lens2':17.5}


def unscaled(x):
    speed,b,k,c1,c2,c3,c4,gap,df,dr=x[:10]
    f1=speed*D; mag=F/f1; sep=(F-b)/(mag+1); q=f1-sep
    r2=-2*q*(sep+b)/(sep+b-q)*(1+dr)
    # Radius, axial thickness, conic, material.
    return [[-2*f1,-sep,k,'mirror'],[r2,sep+x[11]*b,x[10],'mirror'],
            [1/c1,4,0,'N-BK7'],[1/c2,gap,0,'air'],[1/c3,3,0,'N-F2'],
            [1/c4,(1-x[11])*b-7-gap+df,0,'air']]


def scale_factor(x):
    o=optic.Optic(); o.surfaces.add(index=0,thickness=np.inf)
    for i,(r,t,k,mat) in enumerate(unscaled(x),1):
        o.surfaces.add(index=i,radius=r,thickness=t,conic=k,material=mat,is_stop=i==1)
    o.surfaces.add(index=7); o.set_aperture(aperture_type='EPD',value=D)
    o.fields.set_type('angle'); o.fields.add(y=0); o.wavelengths.add(value=.55,is_primary=True)
    return F/abs(float(o.paraxial.f2()))


def build(x,focus=0,finite=False):
    s=scale_factor(x); surfaces=unscaled(x); sep=-surfaces[0][1]*s
    # Entrance annulus lies 3 mm ahead of the secondary vertex; shields the
    # incoming beam. The return beam traverses a separate physical primary hole.
    o=optic.Optic(name='B05 co-designed Cassegrain/corrector, Run 008')
    o.surfaces.add(index=0,thickness=800000 if finite else np.inf)
    o.surfaces.add(index=1,thickness=sep+3,is_stop=True,
                   aperture=RadialAperture(AP['entrance_outer'],AP['obstruction']))
    o.surfaces.add(index=2,radius=surfaces[0][0]*s,thickness=-sep,conic=x[2],material='mirror',
                   aperture=RadialAperture(AP['primary_outer'],AP['hole']))
    o.surfaces.add(index=3,radius=surfaces[1][0]*s,thickness=sep,conic=x[10],material='mirror',
                   aperture=RadialAperture(AP['secondary']))
    o.surfaces.add(index=4,thickness=x[11]*x[1]*s,aperture=RadialAperture(AP['hole']))
    for idx,row in enumerate(surfaces[2:],5):
        r,t,k,mat=row
        o.surfaces.add(index=idx,radius=r*s,thickness=t*s+(focus if idx==8 else 0),material=mat,
                       aperture=RadialAperture(AP['lens1' if idx<7 else 'lens2']))
    o.surfaces.add(index=9)
    o.set_aperture(aperture_type='EPD',value=D)
    o.fields.set_type('angle'); o.fields.add(y=0); o.fields.add(y=ANG)
    for wl in WAVES:o.wavelengths.add(value=wl,is_primary=wl==.55)
    return o


def pupil(n=6):
    # Equal-area annular rings / equal azimuth counts. Stay clear of hard edges
    # in optimization; full-grid audit below covers the edge and vignetting.
    rad=np.sqrt(np.linspace((AP['obstruction']/(D/2)+.012)**2,.99**2,n))
    theta=np.arange(n*4)*2*np.pi/(n*4)
    return (rad[:,None]*np.cos(theta)).ravel(),(rad[:,None]*np.sin(theta)).ravel()


def trace(o,field,wl,n=6):
    px,py=pupil(n)
    r=o.ray_tracer.trace_generic(*field,px,py,wl)
    return np.column_stack([r.x,r.y]),np.asarray(r.i)>0


def merit(x):
    o=build(x); values=[]
    for field in [(0,0),(HX,0),(0,HY),(HX,HY)]:
        data=[trace(o,field,wl) for wl in [.43,.55,.80]]
        center=np.mean(np.concatenate([p[k] for p,k in data]),axis=0)
        for p,k in data:
            delta=np.nan_to_num((p-center)/.01,nan=100,posinf=100,neginf=-100)
            delta[~k]=30
            values.extend(delta.ravel())
    values.extend(np.array(x[3:7])*10)
    return np.asarray(values)


def geometric(x,focus=0,finite=False):
    o=build(x,focus,finite); rows=[]
    for field in FIELDS:
        data=[trace(o,field,wl,14) for wl in WAVES]
        center=np.mean(np.concatenate([p[k] for p,k in data]),axis=0)
        rows.append(dict(field=field,centroid_mm=center.tolist(),
            rms_um=[float(np.sqrt(np.mean(np.sum((p[k]-center)**2,axis=1)))*1000) for p,k in data],
            retained_fraction=[float(np.mean(k)) for p,k in data]))
    return dict(efl_mm=abs(float(o.paraxial.f2())),f_number=abs(float(o.paraxial.f2()))/D,
                worst_rms_um=max(max(r['rms_um']) for r in rows),rows=rows)


def diffraction(x,field,wl,n=96,pad=4):
    o=build(x)
    ps=ScalarFFTPSF(o,field,wl,num_rays=n,grid_size=pad*n,strategy='centroid_sphere',remove_tilt=False)
    pupil_data=np.asarray(ps.pupils[0]); assert np.all(np.isfinite(pupil_data))
    # Matched diffraction reference keeps the actual clipped pupil amplitude
    # and removes phase only. No refocus or best-fit-sphere removal.
    actual=np.asarray(ps.psf,dtype=float); actual/=actual.sum()
    ideal=np.abs(np.fft.fftshift(np.fft.fft2(np.abs(pupil_data),s=actual.shape)))**2
    ideal/=ideal.sum()
    # Optiland accounts for working f/#; its getter returns full width in um.
    extent=ps._get_psf_units(actual); dx=float(extent[0])/actual.shape[1]/1000
    nu=np.fft.fftshift(np.fft.fftfreq(actual.shape[0],d=dx)); mid=len(nu)//2
    def measures(im):
        otf=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(im))); otf/=otf[mid,mid]
        mtfx=np.interp(FREQ,nu[mid:],np.abs(otf[mid,mid:]))
        mtfy=np.interp(FREQ,nu[mid:],np.abs(otf[mid:,mid]))
        # Fractional pixel overlap avoids rounding tiny EE boxes to FFT bins.
        coords=(np.arange(im.shape[0])-mid)*dx
        ee=[]
        for count in [1,2,3]:
            half=count*R['pixel_pitch_um'][0]/2000
            weights=np.maximum(0,np.minimum(coords+dx/2,half)-np.maximum(coords-dx/2,-half))/dx
            ee.append(float(weights@im@weights))
        return dict(mtf_x=mtfx.tolist(),mtf_y=mtfy.tolist(),ee_1_2_3_pixels=ee)
    return dict(field=field,wavelength_um=wl,pupil_samples=n,fft_size=pad*n,dx_um=dx*1000,
                actual=measures(actual),matched_diffraction=measures(ideal),
                relative_peak=float(actual.max()/ideal.max()),
                pupil_nonzero_fraction=float(np.mean(abs(pupil_data)>0)))


def main():
    speed=2.4; magnification=F/(speed*D)
    secondary_conic=-((magnification+1)/(magnification-1))**2
    x=np.array([speed,85,-1,.0005,-.0005,-.0005,.0005,8,0,0,secondary_conic,.45])
    if '--probe' in sys.argv:
        print(json.dumps(geometric(x),indent=2)[:700]); print(json.dumps(diffraction(x,(0,0),.55,64),indent=2)); return
    out=ROOT/'runs/run_008'; out.mkdir(exist_ok=False)
    start=time.monotonic(); timestamp=datetime.now(timezone.utc).isoformat()
    initial=geometric(x)
    (out/'initial.json').write_text(json.dumps(initial,indent=2)+'\n')
    # B05 bounds retain a common packaging screen; secondary conic and lens station are released. EFL is enforced by scale and
    # entrance EPD remains fixed, so first-order fit cannot be sacrificed.
    bounds=([2.,60,-4,-.025,-.025,-.025,-.025,2,-25,-.08,-12,.15],
            [3.5,160,0,.025,.025,.025,.025,25,25,.08,0,.70])
    fit=least_squares(merit,x,bounds=bounds,x_scale='jac',max_nfev=110,ftol=1e-5,xtol=1e-6,gtol=1e-5)
    best=geometric(fit.x)
    (out/'configuration.json').write_text(json.dumps(dict(initial=x.tolist(),best=fit.x.tolist(),bounds=bounds,
        physical_radii_mm=AP,scale=scale_factor(fit.x),wavelengths_um=WAVES,fields=FIELDS),indent=2)+'\n')
    (out/'optimization.json').write_text(json.dumps(dict(initial=initial,best=best,nfev=fit.nfev,
        message=fit.message,seconds=time.monotonic()-start),indent=2)+'\n')
    print('Physical co-design:',best['efl_mm'],best['worst_rms_um'],flush=True)
    # Finite-conjugate detector-only refocus, common plane across all fields/colors.
    def focus_merit(delta):
        o=build(fit.x,delta,True); score=0
        for field in [(0,0),(HX,HY)]:
            data=[trace(o,field,wl,8) for wl in [.43,.55,.80]]
            pts=np.concatenate([p[k] for p,k in data]); score+=float(np.mean(np.sum((pts-pts.mean(axis=0))**2,axis=1)))
        return score
    finite=minimize_scalar(focus_merit,bounds=(-1,3),method='bounded',options={'xatol':1e-5,'maxiter':40})
    (out/'finite_800m.json').write_text(json.dumps(dict(detector_shift_mm=float(finite.x),
        success=bool(finite.success),metrics=geometric(fit.x,float(finite.x),True),
        note='800 m from entrance reference plane; compound-system ray trace, not thin lens estimate'),indent=2)+'\n')
    diffs=[]
    for field in [(0,0),(HX,0),(0,HY),(HX,HY)]:
        for wl in WAVES:
            diffs.append(diffraction(fit.x,field,wl))
        print('Diffraction field complete',field,flush=True)
    (out/'diffraction.json').write_text(json.dumps(dict(frequencies_lpmm=FREQ.tolist(),rows=diffs,
        note='Monochromatic, centroid-sphere reference at fixed image plane; energy-normalized scalar FFT, no detector MTF. No broadband MTF claimed.'),indent=2,allow_nan=False)+'\n')
    checks=[diffraction(fit.x,(0,0),.55,160),diffraction(fit.x,(HX,HY),.80,160)]
    (out/'sampling_check.json').write_text(json.dumps(checks,indent=2)+'\n')
    o=build(fit.x)
    with (out/'prescription.csv').open('w',newline='') as file:
        writer=csv.writer(file); writer.writerow(['index','radius_mm','thickness_mm','conic','aperture'])
        for i,s in enumerate(o.surfaces):writer.writerow([i,s.geometry.radius,s.thickness,getattr(s.geometry,'k',0),str(s.aperture.to_dict()) if s.aperture else 'none'])
    shutil.copy2(__file__,out/'model.py'); shutil.copy2(ROOT/'requirements/eo_requirements.yaml',out/'requirements.yaml')
    (out/'metadata.json').write_text(json.dumps(dict(track='B',candidate_ids=['B05'],run_id='008',parent_run=None,stage='screening',
        purpose='Screen independently seeded co-designed two-conic Cassegrain and two-lens corrector against B04',start_utc=timestamp,
        end_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-start,
        substantial_search_count=2,materially_distinct_attempt_count=1,candidate_stage_attempts_total=1,
        searches=['physical joint design','finite-conjugate scalar refocus'],plateau=False,
        assumptions=['Seed: primary f/2.4, backfocus 85 mm, paraboloid, secondary classical conic derived from magnification; weak lenses', 'No B04 optimized geometry used; shared analysis implementation only','Fixed mechanical aperture sizes','Ideal coatings/no spider or detailed baffles','Equal spectral weights for geometric merit',
        'Uniform geometric scale enforces 550 nm paraxial EFL; aperture diameter fixed'],
        versions={'python':sys.version,'optiland':optiland.__version__,'numpy':np.__version__,'scipy':scipy.__version__},
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')


if __name__=='__main__':main()
