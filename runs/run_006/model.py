"""B04 fresh CDK screen. Independent analytic seed; no Track A inputs.

Configured WSL Python only. Screening objectives/variable bounds are engineering
assumptions. This first model has no mechanical aperture clipping: it is NOT a
physical validation and cannot be promoted on RMS alone.
"""
import json, time, sys, hashlib, shutil, platform
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import least_squares
import scipy, yaml, optiland
from optiland import optic

ROOT=next(p for p in Path(__file__).resolve().parents if (p / 'WORK_GUIDE.md').is_file())
REQ=yaml.safe_load((ROOT/'requirements/eo_requirements.yaml').read_text())['source_explicit_requirements']
F=REQ['pixel_pitch_um'][0]*1000/REQ['instantaneous_fov_urad_per_pixel']
D=F/REQ['f_number']
W,H=np.array(REQ['array_px'])*REQ['pixel_pitch_um'][0]/1000
ANGLE=np.degrees(np.arctan(np.hypot(W,H)/2/F))
WAVES=[.43,.50,.55,.65,.725,.80]
FIELDS=[(0,0),(.5*W/np.hypot(W,H),.5*H/np.hypot(W,H)),(W/np.hypot(W,H),0),(W/np.hypot(W,H),H/np.hypot(W,H))]


def build(x):
    # x: primary f-number, backfocus, K1, four lens curvatures, gap,
    #     focal-plane correction, secondary-power fractional correction.
    speed,b,k,c1,c2,c3,c4,gap,df,dr=x
    f1=speed*D; m=F/f1
    sep=(F-b)/(m+1); q=f1-sep; image=sep+b
    r2=-2*q*image/(image-q)*(1+dr)
    o=optic.Optic(name='Independent Track B B04 CDK')
    o.surfaces.add(index=0,radius=np.inf,thickness=np.inf)
    o.surfaces.add(index=1,radius=-2*f1,conic=k,thickness=-sep,material='mirror',is_stop=True)
    o.surfaces.add(index=2,radius=r2,conic=0,thickness=sep+b*.35,material='mirror')
    radius=lambda c: np.inf if abs(c)<1e-10 else 1/c
    o.surfaces.add(index=3,radius=radius(c1),thickness=4,material='N-BK7')
    o.surfaces.add(index=4,radius=radius(c2),thickness=gap)
    o.surfaces.add(index=5,radius=radius(c3),thickness=3,material='N-F2')
    o.surfaces.add(index=6,radius=radius(c4),thickness=b*.65-7-gap+df)
    o.surfaces.add(index=7)
    o.set_aperture(aperture_type='EPD',value=D)
    o.fields.set_type('angle'); o.fields.add(y=0); o.fields.add(y=ANGLE)
    for wl in WAVES: o.wavelengths.add(value=wl,is_primary=wl==.55)
    return o


def xy(o,hx,hy,wl,n=5):
    r=o.trace(Hx=hx,Hy=hy,wavelength=wl,num_rays=n,distribution='hexapolar')
    xy=np.column_stack([np.asarray(r.x),np.asarray(r.y)])
    if not np.all(np.isfinite(xy)): raise ValueError('nonfinite trace')
    return xy


def residual(x):
    o=build(x); values=[]
    for hx,hy in FIELDS:
        # One common image centroid across the wavelengths penalizes lateral color.
        points=[xy(o,hx,hy,wl) for wl in [.43,.55,.80]]
        center=np.mean(np.concatenate(points),axis=0)
        for pts in points: values.extend(((pts-center)/.01).ravel())
        # Field scale is a constraint proxy rather than an RMS trade target.
        target=F*np.tan(np.radians(ANGLE))*np.array([hx,hy])
        values.extend((np.abs(center)-np.abs(target))/.01)
    # Keep lens powers modest; this is a soft manufacturability regularizer.
    values.extend(np.array(x[3:7])*10)
    return np.asarray(values)


def audit(x,n=12):
    o=build(x); rows=[]
    for hx in [-W/np.hypot(W,H),0,W/np.hypot(W,H)]:
        for hy in [-H/np.hypot(W,H),0,H/np.hypot(W,H)]:
            pts=[xy(o,hx,hy,wl,n) for wl in WAVES]
            centroid=np.concatenate(pts).mean(axis=0)
            rms=[float(np.sqrt(np.mean(np.sum((p-centroid)**2,axis=1)))*1000) for p in pts]
            rows.append(dict(field_normalized=[hx,hy],rms_um_by_wavelength=rms,centroid_mm=centroid.tolist()))
    tiny=xy(o,0,1e-4,.55,n).mean(axis=0)
    efl=abs(tiny[1]/np.tan(np.radians(ANGLE*1e-4)))
    return dict(worst_rms_um=max(max(row['rms_um_by_wavelength']) for row in rows),
                efl_finite_difference_mm=efl,f_number=efl/D,fields=rows,
                optical_model='Unclipped rotational model; common detector plane and centroid across wavelengths',
                physical_validity='UNVERIFIED: primary hole, entrance obstruction and clear apertures not applied',
                mtf=None,ensquared_energy=None,temperature_compliance='unverified',focus_800m='unverified')


def main():
    if '--probe' in sys.argv:
        x=[2.5,100,-.7,.002,-.002,-.002,.002,8,0,0]
        print('Residual length',len(residual(x))); print(json.dumps(audit(x,5),indent=2)[:700])
        return
    out=ROOT/'runs/run_006'; out.mkdir(exist_ok=False)
    start=time.monotonic(); timestamp=datetime.now(timezone.utc).isoformat()
    x=np.array([2.5,100,-.7,.002,-.002,-.002,.002,8,0,0])
    bounds=([2.,60,-.999,-.025,-.025,-.025,-.025,2,-25,-.08],
            [3.5,160,-.01,.025,.025,.025,.025,25,25,.08])
    initial=audit(x); records=[]
    # One bounded joint solve. Follow-ups require a new engineering strategy,
    # not arbitrary random restarts. max_nfev is a hard reproducibility bound.
    fit=least_squares(residual,x,bounds=bounds,x_scale='jac',max_nfev=65,
                      ftol=1e-5,xtol=1e-6,gtol=1e-5)
    result=audit(fit.x)
    print('B04 attempt 1 complete:',result['worst_rms_um'],'um; EFL',result['efl_finite_difference_mm'],flush=True)
    records.append(dict(attempt=1,strategy='Joint mirror geometry/primary ellipsoid and two separated spherical lenses',
                        x=fit.x.tolist(),nfev=fit.nfev,cost=fit.cost,message=fit.message,
                        elapsed_seconds=time.monotonic()-start,metrics=result))
    (out/'metrics.json').write_text(json.dumps(dict(initial=initial,attempts=records),indent=2,allow_nan=False)+'\n')
    config=dict(parameter_names=['primary_f_number','paraxial_backfocus_mm','primary_conic','lens1_front_curvature',
                'lens1_back_curvature','lens2_front_curvature','lens2_back_curvature','lens_gap_mm',
                'detector_shift_mm','secondary_radius_fractional_change'],initial=x.tolist(),best=fit.x.tolist(),
                bounds=bounds,wavelengths_um=WAVES,screen_fields=FIELDS,merit='10 um spot normalization + 10 um field-scale proxy, modest curvature regularizer',
                seed_derivation='f1=speed*D; M=F/f1; separation=(F-backfocus)/(M+1); q=f1-separation; R2=-2*q*(separation+backfocus)/(separation+backfocus-q)',
                assumptions='Primary speed 2.5/backfocus 100 mm initial, broad bounded variables, 4/3 mm lens thickness, BK7/F2; no customer limits implied')
    (out/'configuration.json').write_text(json.dumps(config,indent=2)+'\n')
    o=build(fit.x)
    with (out/'prescription.csv').open('w') as file:
        file.write('index,radius_mm,thickness_mm,conic\n')
        for i,s in enumerate(o.surfaces):
            file.write(f'{i},{s.geometry.radius},{s.thickness},{getattr(s.geometry, "k", 0)}\n')
    shutil.copy2(__file__,out/'model.py')
    shutil.copy2(ROOT/'requirements/eo_requirements.yaml',out/'requirements.yaml')
    (out/'metadata.json').write_text(json.dumps(dict(track='B',run_id='006',candidate_ids=['B04'],
        stage='screening',purpose='Does a fresh jointly designed two-lens CDK seed warrant development?',
        start_utc=timestamp,end_utc=datetime.now(timezone.utc).isoformat(),active_compute_seconds=time.monotonic()-start,
        substantial_search_count=1,materially_distinct_attempt_count=1,plateau=False,parent_run=None,
        preceding_screen='005',track_a_seed_used=False,reference_accessed=False,
        versions=dict(python=sys.version,optiland=optiland.__version__,numpy=np.__version__,scipy=scipy.__version__),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')


if __name__=='__main__':main()
