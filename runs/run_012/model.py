"""B09 stock-nominal 130/650 paraboloid + flat and custom spherical extender.
No Track A or optimized B05/B06 geometry is imported. Unfolded flat isometry is
used for the solve/FFT; a true 45-degree fold is independently ray checked.
"""
import sys,json,time,hashlib,shutil,csv
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.optimize import least_squares,minimize_scalar
from optiland import optic
from optiland.physical_apertures import RadialAperture,EllipticalAperture
from optiland.psf import ScalarFFTPSF
import yaml,optiland,scipy
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists());OUT=ROOT/'runs/run_012'
REQ=yaml.safe_load((ROOT/'requirements/eo_requirements.yaml').read_text())['source_explicit_requirements']
F=REQ['pixel_pitch_um'][0]*1000/REQ['instantaneous_fov_urad_per_pixel'];D=F/REQ['f_number']
W,H=np.array(REQ['array_px'])*REQ['pixel_pitch_um'][0]/1000;ANG=np.degrees(np.arctan(np.hypot(W,H)/(2*F)))
HX=np.degrees(np.arctan(W/(2*F)))/ANG;HY=np.degrees(np.arctan(H/(2*F)))/ANG
FIELDS=[(x*HX,y*HY) for x in [-1,0,1] for y in [-1,0,1]];WAVES=[.43,.5,.55,.65,.725,.8];FREQ=np.array([50,100,150,1000/(2*REQ['pixel_pitch_um'][0])])
PRIMARY_F=650.;PRIMARY_D=130.;FLAT_DISTANCE=480.;FLAT_MINOR=47.;VANE=.5;LENS_RADIUS=17.5

class NewtonianPupil(RadialAperture):
    def __init__(self):
        super().__init__(D/2,0);self.set_field(0,0)
    def set_field(self,hx,hy):
        self.l=float(np.tan(np.radians(ANG*hx)));self.m=float(np.tan(np.radians(ANG*hy)))
    def contains(self,x,y):
        # Back-project the physical 45-degree flat and plane spider to the
        # entrance pupil at the primary, including field-dependent shadows.
        t=(-FLAT_DISTANCE-x)/(1+self.l);xf=x+t*self.l;yf=y+t*self.m
        clear_flat=xf*xf+yf*yf>(FLAT_MINOR/2)**2
        xs=x-FLAT_DISTANCE*self.l;ys=y-FLAT_DISTANCE*self.m
        return super().contains(x,y)&clear_flat&(abs(xs)>=VANE/2)&(abs(ys)>=VANE/2)
    def to_dict(self):return dict(type='NewtonianPupil',r_max=self.r_max,r_min=self.r_min,vane_width_mm=VANE,
        note='Field-dependent projected 45-degree flat and orthogonal plane spider; substrate/cell footprint requires drawing')

def save(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def sag(c,r):return c*r*r/(1+np.sqrt(1-c*c*r*r))
def physical(x):
    c1,c2,c3,c4,s,g,q=x
    return dict(lens_edge_thickness_mm=[4+sag(c2,LENS_RADIUS)-sag(c1,LENS_RADIUS),3+sag(c4,LENS_RADIUS)-sag(c3,LENS_RADIUS)],
        airgap_edge_mm=g+sag(c3,LENS_RADIUS)-sag(c2,LENS_RADIUS),image_path_from_primary_mm=s+7+g+q,
        folded_first_lens_x_mm=s-FLAT_DISTANCE,folded_detector_x_mm=s+7+g+q-FLAT_DISTANCE,
        primary_to_flat_mm=FLAT_DISTANCE)

def build(x,focus=0,finite=False,folded=False):
    c1,c2,c3,c4,s,g,q=x;o=optic.Optic(name='B09 fixed stock-nominal paraboloid and small custom extender')
    o.surfaces.add(index=0,thickness=800000 if finite else np.inf)
    o.surfaces.add(index=1,thickness=.01,is_stop=True,aperture=NewtonianPupil())
    o.surfaces.add(index=2,radius=-1300,conic=-1,thickness=-FLAT_DISTANCE,material='mirror',aperture=RadialAperture(PRIMARY_D/2))
    o.surfaces.add(index=3,thickness=-(s-FLAT_DISTANCE),aperture=RadialAperture(FLAT_MINOR/2))
    for i,c,t,mat in [(4,c1,4,'N-BK7'),(5,c2,g,'air'),(6,c3,3,'N-F2'),(7,c4,q+focus,'air')]:
        o.surfaces.add(index=i,radius=-1/c if abs(c)>1e-14 else np.inf,thickness=-t,material=mat,aperture=RadialAperture(LENS_RADIUS))
    o.surfaces.add(index=8)
    o.set_aperture(aperture_type='EPD',value=D);o.fields.set_type('angle');o.fields.add(y=0);o.fields.add(y=ANG)
    for wl in WAVES:o.wavelengths.add(value=wl,is_primary=wl==.55)
    if folded:
        # Mirror reflection of the unfolded downstream space through the plane
        # z+x=zflat: unfolded Z becomes X=zflat-Z. Local z -> +X.
        from optiland.materials import IdealMaterial
        o.surfaces[3].material_post=IdealMaterial(n=-1)
        o.surfaces[3].geometry.cs.ry=np.pi/4
        o.surfaces[3].aperture=EllipticalAperture(FLAT_MINOR/np.sqrt(2),FLAT_MINOR/2)
        zflat=float(o.surfaces[3].geometry.cs.z)
        for i in range(4,9):
            geom=o.surfaces[i].geometry;oldz=float(geom.cs.z);geom.cs.x=zflat-oldz;geom.cs.z=zflat;geom.cs.ry=np.pi/2
            geom.radius=-geom.radius
    return o

def pupil(n=5):
    r=np.sqrt((np.arange(n)+.5)/n);th=(np.arange(4*n)+.5)*2*np.pi/(4*n)
    return (r[:,None]*np.cos(th)).ravel(),(r[:,None]*np.sin(th)).ravel()
def trace(o,field,wl,n=5):
    o.surfaces[1].aperture.set_field(*field)
    px,py=pupil(n);rr=o.ray_tracer.trace_generic(*field,px,py,wl)
    return np.column_stack([rr.x,rr.y]),(np.asarray(rr.i)>0)
def merit(x):
    try:
        o=build(x);values=[]
        for field in [(0,0),(HX,0),(0,HY),(HX,HY)]:
            data=[trace(o,field,wl,6) for wl in [.43,.55,.8]];pts=np.array([p for p,k in data]);center=np.concatenate([p[k] for p,k in data]).mean(axis=0)
            px,py=pupil(6);expected=o.surfaces[1].aperture.contains(px*D/2,py*D/2)
            delta=(pts-center)/.005;delta[:,~expected]=0
            values.extend(delta.ravel())
            values.extend([30*float(np.mean(expected&~k)) for p,k in data])
        values.append((abs(float(o.paraxial.f2()))-F)/.01)
        ph=physical(x)
        values.extend([max(0,.8-t)*50 for t in ph['lens_edge_thickness_mm']]);values.append(max(0,.5-ph['airgap_edge_mm'])*50)
        return np.nan_to_num(values,nan=1e5,posinf=1e5,neginf=-1e5)
    except (ValueError,FloatingPointError):return np.full(3472,1e5)

def geometric(x,focus=0,finite=False,n=10,fields=FIELDS):
    o=build(x,focus,finite);rows=[]
    for field in fields:
        data=[trace(o,field,wl,n) for wl in WAVES];center=np.concatenate([p[k] for p,k in data]).mean(axis=0)
        rows.append(dict(field=field,rms_um=[float(np.sqrt(np.mean(np.sum((p[k]-center)**2,axis=1)))*1000) for p,k in data],
            centroid_mm=center.tolist(),survival=[float(k.mean()) for p,k in data]))
    return dict(efl_mm=abs(float(o.paraxial.f2())),f_number=abs(float(o.paraxial.f2()))/D,
        worst_rms_um=max(max(r['rms_um']) for r in rows),rows=rows,physical=physical(x))

def diffraction(x,field,wl,n=192,focus=0):
    o=build(x,focus);o.surfaces[1].aperture.set_field(*field)
    p=ScalarFFTPSF(o,field,wl,num_rays=n,grid_size=4*n,strategy='centroid_sphere',remove_tilt=False,robust_trim_std=0)
    data=p.get_data(field,wl);phase=np.asarray(data.opd);amp=np.sqrt(np.asarray(data.intensity));mask=amp>0;assert np.isfinite(phase[mask]).all()
    axis=np.linspace(-1,1,n);xx,yy=np.meshgrid(axis,axis);disk=xx*xx+yy*yy<=1;v=np.zeros_like(phase,complex);v[mask]=amp[mask]*np.exp(-2j*np.pi*phase[mask]);pupil=np.zeros((n,n),complex);pupil[disk]=v
    step=wl*.001*abs(float(o.paraxial.f2()))/D*(n-1)/(n*4);size=n*4;mid=size//2;freq=np.fft.fftshift(np.fft.fftfreq(size,d=step));coords=(np.arange(size)-mid)*step;half=REQ['pixel_pitch_um'][0]/1000
    weights=np.maximum(0,np.minimum(coords+step/2,half)-np.maximum(coords-step/2,-half))/step
    def calc(p):
        im=abs(np.fft.fftshift(np.fft.fft2(p,s=(size,size))))**2;im/=im.sum();otf=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(im)));otf/=otf[mid,mid]
        return dict(mtf_x=np.interp(FREQ,freq[mid:],abs(otf[mid,mid:])).tolist(),mtf_y=np.interp(FREQ,freq[mid:],abs(otf[mid:,mid])).tolist(),ee2=float(weights@im@weights))
    return dict(field=field,wavelength_um=wl,pupil_grid=n,actual=calc(pupil),matched=calc(abs(pupil)))

def main():
    seed=np.array([-.004,.004,.0021,-.0021,550.,10.,125.])
    if '--probe' in sys.argv:print(json.dumps(geometric(seed),indent=2));return
    if (OUT/'attempt_01.json').exists():print('Completed solve retained');return
    start=datetime.now(timezone.utc);save('initial.json',dict(parameters=seed.tolist(),metrics=geometric(seed)))
    low=[-.035]*4+[550,1,40];high=[.035]*4+[600,45,230]
    fit=least_squares(merit,seed,bounds=(low,high),x_scale='jac',max_nfev=120,ftol=1e-6,xtol=1e-7,gtol=1e-6)
    result=dict(parameters=fit.x.tolist(),bounds=[low,high],metrics=geometric(fit.x),nfev=fit.nfev,success=bool(fit.success),message=fit.message)
    save('attempt_01.json',result);save('metadata.json',dict(track='B',run_id='012',candidate_ids=['B09'],stage='hybrid development',status='IN_PROGRESS',
        start_utc=start.isoformat(),last_checkpoint_utc=datetime.now(timezone.utc).isoformat(),substantial_search_count=1,materially_distinct_attempt_count=1,
        primary_radius_mm=-1300,primary_conic=-1,stock_nominal_not_measured=True,primary_optimized=False,glass_choices=['N-BK7','N-F2'],
        model_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),versions=dict(python=sys.version,optiland=optiland.__version__,scipy=scipy.__version__)))
    shutil.copy2(__file__,OUT/'model.py');print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
