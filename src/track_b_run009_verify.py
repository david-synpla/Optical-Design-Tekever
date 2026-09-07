"""Resume and validate saved B06; never re-run its completed conic search.
Uses explicit physical subaperture, dense ray sampling and entrance-pupil FFT.
"""
import sys,json,csv,shutil,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.optimize import minimize_scalar
from optiland.psf import ScalarFFTPSF
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import track_b_run009_tma as m

OUT=m.ROOT/'runs/run_009'
SAVED=json.loads((OUT/'attempt_01.json').read_text()); SEED=SAVED['seed']; V=SAVED['parameters']; APS=SAVED['metrics']['apertures']
WAVES=[.43,.50,.55,.65,.725,.80];FREQ=np.array([50,100,150,1000/(2*m.REQ['pixel_pitch_um'][0])])


def build(delta=0,finite=False):
    o=m.build(SEED,V[:3],V[3]+delta,APS)
    if finite:o.updater.set_thickness(800000,0)
    return o


def finite_trace(o,field,n):
    # Finite object arithmetic can place an exact rim ray just outside the stop.
    # Move samples inward by 1e-9 of radius (0.064 nm); apertures stay unchanged.
    px,py=m.pupil(SEED,n);cy=SEED['offset']/(SEED['offset']+m.D/2)
    r=o.ray_tracer.trace_generic(*field,px*(1-1e-9),cy+(py-cy)*(1-1e-9),.55)
    pts=np.column_stack([r.x,r.y])
    return pts,np.isfinite(pts).all(axis=1)&(np.asarray(r.i)>0)


def diffraction(field,wl,n=256,pad=4):
    o=build()
    ps=ScalarFFTPSF(o,field,wl,num_rays=n,grid_size=n*pad,strategy='centroid_sphere',remove_tilt=False,robust_trim_std=0)
    data=ps.get_data(field,wl)
    phase=np.asarray(data.opd);amp=np.sqrt(np.asarray(data.intensity))
    assert np.all(np.isfinite(phase)[amp>0])
    axis=np.linspace(-1,1,n);xx,yy=np.meshgrid(axis,axis);disk=xx*xx+yy*yy<=1
    pupil=np.zeros((n,n),complex);values=np.zeros_like(phase,dtype=complex)
    mask=amp>0;values[mask]=amp[mask]*np.exp(-2j*np.pi*phase[mask]);pupil[disk]=values
    # Physical Fourier scaling from entrance-pupil coordinates, NOT treating
    # the virtual parent EPD as a 358 mm physical telescope aperture.
    step=wl*1e-3*m.F/(2*(SEED['offset']+m.D/2))*(n-1)/(n*pad)
    size=n*pad;mid=size//2;freq=np.fft.fftshift(np.fft.fftfreq(size,d=step))
    def calculate(p):
        im=abs(np.fft.fftshift(np.fft.fft2(p,s=(size,size))))**2;im/=im.sum()
        otf=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(im)));otf/=otf[mid,mid]
        mtfx=np.interp(FREQ,freq[mid:],abs(otf[mid,mid:]));mtfy=np.interp(FREQ,freq[mid:],abs(otf[mid:,mid]))
        coords=(np.arange(size)-mid)*step;ee=[]
        for count in [1,2,3]:
            half=count*m.REQ['pixel_pitch_um'][0]/2000
            weights=np.maximum(0,np.minimum(coords+step/2,half)-np.maximum(coords-step/2,-half))/step
            ee.append(float(weights@im@weights))
        return dict(mtf_x=mtfx.tolist(),mtf_y=mtfy.tolist(),ee_1_2_3_pixels=ee)
    actual=calculate(pupil);ideal=calculate(abs(pupil))
    normalized=FREQ*(wl*.001*m.REQ['f_number'])
    theory=2/np.pi*(np.arccos(normalized)-normalized*np.sqrt(1-normalized**2))
    return dict(field=field,wavelength_um=wl,parent_pupil_grid=n,physical_pupil_samples_approx=n*m.D/(2*(SEED['offset']+m.D/2)),
        fft_grid=size,dx_um=step*1000,actual=actual,matched_diffraction=ideal,clear_circle_analytic_mtf=theory.tolist(),
        ideal_vs_analytic_max_error=max(float(np.max(abs(np.array(ideal[k])-theory))) for k in ['mtf_x','mtf_y']))


def dense_geometry(delta=0,finite=False,n=65,field_count=5):
    o=build(delta,finite);rows=[];hist=[]
    for hx in np.linspace(-m.HX,m.HX,field_count):
        for hy in np.linspace(-m.HY,m.HY,field_count):
            pts,keep=finite_trace(o,(hx,hy),n) if finite else m.trace(o,SEED,(hx,hy),n)
            assert np.all(keep),'Physical aperture clipped a sampled science ray'
            rows.append(dict(field=[hx,hy],rms_um=float(np.sqrt(np.mean(np.sum((pts-pts.mean(axis=0))**2,axis=1)))*1000),
                             centroid_mm=pts.mean(axis=0).tolist(),survival=float(keep.mean())))
            hist.append((np.array(o.surfaces.x),np.array(o.surfaces.y),np.array(o.surfaces.z)))
    return dict(rows=rows,worst_rms_um=max(r['rms_um'] for r in rows)),hist


def clearance(hist):
    # Same conservative cylindrical slabs as initial audit, but now include
    # source-to-entrance segment 0->1 as well as every later nonincident pass.
    obs=SAVED['metrics']['obstacles'];minimum=1e9;limiter=None
    for xx,yy,zz in hist:
        for i in range(0,5):
            for ob in obs:
                if ob['index'] in [i,i+1]:continue
                dz=zz[i+1]-zz[i];a=(ob['zlo']-zz[i])/dz;b=(ob['zhi']-zz[i])/dz
                low=np.maximum(0,np.minimum(a,b));high=np.minimum(1,np.maximum(a,b));ok=low<=high
                if not np.any(ok):continue
                bx=xx[i]-ob['x'];by=yy[i]-ob['y'];vx=xx[i+1]-xx[i];vy=yy[i+1]-yy[i]
                t=np.clip(-(bx*vx+by*vy)/np.maximum(vx*vx+vy*vy,1e-30),low,high)
                dist=np.hypot(bx+t*vx,by+t*vy)-ob['radius'];d=float(min(dist[ok]))
                if d<minimum:minimum=d;limiter=[i,i+1,ob['index']]
    return dict(minimum_clearance_mm=minimum,limiting_segment_obstacle=limiter,
                margins='2 mm mirror radius/slab and 1 mm detector radial/slab margins; screening assumptions')


def main():
    if '--probe' in sys.argv:
        print(json.dumps(diffraction((0,0),.55,192),indent=2));return
    start=time.monotonic();geo,hist=dense_geometry();clear=clearance(hist)
    (OUT/'dense_geometry.json').write_text(json.dumps(dict(metrics=geo,clearance=clear),indent=2)+'\n')
    rows=[]
    for field in [(0,0),(m.HX,0),(0,m.HY),(m.HX,m.HY),(m.HX,-m.HY)]:
        for wl in WAVES:rows.append(diffraction(field,wl))
        print('B06 diffraction field complete',field,flush=True)
    (OUT/'diffraction.json').write_text(json.dumps(dict(frequencies_lpmm=FREQ.tolist(),rows=rows,
        note='Monochromatic fixed-plane scalar diffraction; physical 128.097 mm pupil, ideal mirror amplitudes, no polarization/coating/scatter. No broadband MTF claimed.'),indent=2)+'\n')
    fine=[diffraction((0,0),.55,384),diffraction((m.HX,m.HY),.43,384)]
    (OUT/'sampling_check.json').write_text(json.dumps(fine,indent=2)+'\n')
    def focus_merit(delta):
        o=build(delta,True);score=0
        for field in [(0,0),(m.HX,m.HY),(m.HX,-m.HY)]:
            pts,keep=finite_trace(o,field,17);assert np.all(keep)
            score+=np.mean(np.sum((pts-pts.mean(axis=0))**2,axis=1))
        return score
    fit=minimize_scalar(focus_merit,bounds=(-1,3),method='bounded',options={'xatol':1e-5,'maxiter':40})
    finite,_=dense_geometry(float(fit.x),True,33,5)
    (OUT/'finite_800m.json').write_text(json.dumps(dict(detector_shift_along_final_beam_mm=float(fit.x),
        detector_global_z_shift_mm=-float(fit.x),success=bool(fit.success),metrics=finite,
        note='Object 800 m from entrance plane; detector-only refocus, no mechanism implied'),indent=2)+'\n')
    o=build();pos=np.asarray(o.surfaces.positions).ravel();origin=pos[2]
    shape=[];fig,ax=plt.subplots(figsize=(10,5))
    def sag(rad,curvature,k):return curvature*rad*rad/(1+np.sqrt(1-(1+k)*curvature*curvature*rad*rad))
    for i,ap in zip([2,3,4],APS):
        g=o.surfaces[i].geometry;c=1/float(g.radius);k=float(g.k)
        y=np.linspace(ap['y']-ap['radius'],ap['y']+ap['radius'],600);z=sag(abs(y),c,k)
        ax.plot(pos[i]-origin+z,y,'k-',lw=2)
        spherical=sag(abs(y),c,0);valid=np.isfinite(spherical)
        shape.append(dict(surface=i,radius_mm=float(g.radius),conic=k,patch_center_y_mm=ap['y'],patch_radius_mm=ap['radius'],
            parent_radial_extent_mm=abs(ap['y'])+ap['radius'],max_meridional_slope=float(max(abs(np.gradient(z,y)))),
            vertex_sphere_departure_um=float(max(abs(z[valid]-spherical[valid])))*1000,
            note='Departure over off-axis meridian relative to parent vertex-radius sphere, NOT best-fit sphere or figure tolerance'))
    for field,col in [((0,0),'tab:blue'),((0,m.HY),'tab:orange')]:
        parent=SEED['offset']+m.D/2;py=(SEED['offset']+m.D/2*np.array([-.99,-.5,0,.5,.99]))/parent
        rr=o.ray_tracer.trace_generic(*field,np.zeros_like(py),py,.55)
        for j in range(len(py)):ax.plot(np.asarray(o.surfaces.z)[:,j]-origin,np.asarray(o.surfaces.y)[:,j],color=col,lw=.6)
    center=SAVED['metrics']['detector_center_mm'];ax.plot([pos[-1]-origin]*2,[center[1]-m.H/2,center[1]+m.H/2],'r-',lw=3)
    ax.set(xlabel='Z from primary parent vertex (mm)',ylabel='Y from parent axis (mm)',title='B06 off-axis mirror patches and full incoming/return paths')
    ax.set_aspect('equal',adjustable='datalim');fig.tight_layout();fig.savefig(OUT/'layout.png',dpi=150)
    (OUT/'manufacturing.json').write_text(json.dumps(dict(mirrors=shape,vertex_extent_mm=float(max(pos[1:])-min(pos[1:])),
        note='Parent aspheres require off-axis patches and dedicated datums/metrology; no structure, coatings or thermal model'),indent=2)+'\n')
    with (OUT/'prescription.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['surface','radius_mm','thickness_mm','conic','material','aperture'])
        for i,s in enumerate(o.surfaces):writer.writerow([i,s.geometry.radius,s.thickness,getattr(s.geometry,'k',0),'mirror' if i in [2,3,4] else 'air',str(s.aperture.to_dict()) if s.aperture else 'none'])
    shutil.copy2(__file__,OUT/'verify.py')
    (OUT/'resume_verification.json').write_text(json.dumps(dict(resumed_utc=datetime.now(timezone.utc).isoformat(),
        completed_optimizer_repeated=False,prior_json_and_hash_passed=True,prior_replay_passed=True,
        explicit_pupil_dense_trace_passed=True,verification_seconds=time.monotonic()-start,
        additional_search_count=1,additional_distinct_architecture_attempts=0,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
    print('B06 verified',geo['worst_rms_um'],clear,'finite shift',fit.x,flush=True)


if __name__=='__main__':main()
