"""Matched engineering sensitivity; exact saved Track B shapes, no shape solve.
Run with configured WSL Python. Checkpoints are read on resume, not recomputed.
"""
import sys,json,copy,hashlib,importlib.util,time,csv
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.stats import qmc
from optiland.psf import ScalarFFTPSF
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
OUT=ROOT/'runs/run_010'
def load_model(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
A=load_model('b05_saved','runs/run_008/model.py');B=load_model('b06_saved','runs/run_009/model.py')
S=json.loads((ROOT/'runs/run_009/attempt_01.json').read_text());F=A.F;D=A.D
FIELDS=A.FIELDS;WAVES=A.WAVES;FREQ=A.FREQ
def save(path,data):
    path=OUT/path;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def read(path):return json.loads((OUT/path).read_text())
def sag(r,R,k):return r*r/R/(1+np.sqrt(1-(1+k)*(r/R)**2))

class Candidate:
    def __init__(self,cid):
        self.cid=cid;self.b06=cid=='B06'
        if self.b06:self.nom=B.build(S['seed'],S['parameters'][:3],S['parameters'][3],S['metrics']['apertures'])
        else:
            folder='runs/run_008'+('/attempt_02' if cid=='B05-2' else '')
            self.x=json.loads((ROOT/folder/'configuration.json').read_text())['best'];self.nom=A.build(self.x)
        self.parentD=2*(S['seed']['offset']+D/2) if self.b06 else D
        self.groups={'primary':[2],'secondary':[3]}
        if self.b06:self.groups['tertiary']=[4]
        else:self.groups.update(lens1=[5,6],lens2=[7,8],corrector=[5,6,7,8])
        self.groups['detector']=[len(self.nom.surfaces)-1]
        self.defs=[]
        for name,ids in self.groups.items():
            for mode in ['z','x','y','tx','ty']:
                if name=='corrector' and mode!='z':continue
                self.defs.append(dict(name=name+'_'+mode,group=name,mode=mode,step=.01 if len(mode)==1 else .0001,
                    unit='mm' if len(mode)==1 else 'rad'))
            if self.b06 and name!='detector':self.defs.append(dict(name=name+'_clock',group=name,mode='clock',step=.0001,unit='rad'))
        for i in ([2,3,4] if self.b06 else [2,3,5,6,7,8]):
            self.defs.append(dict(name=f's{i}_radius',surface=i,mode='radius',step=1e-4,unit='fractional radius'))
            if i in ([2,3,4] if self.b06 else [2,3]):self.defs.append(dict(name=f's{i}_conic',surface=i,mode='conic',step=.001,unit='absolute K'))
        if not self.b06:
            for i in [5,7]:
                self.defs.extend([dict(name=f's{i}_index',surface=i,mode='index',step=1e-4,unit='absolute index'),
                    dict(name=f's{i}_thickness',surface=i,mode='thickness',step=.01,unit='mm')])
        self.byname={d['name']:d for d in self.defs}

    def build(self,errors={}):
        o=copy.deepcopy(self.nom)
        # Accumulate body transforms so perturbations and adjustments compose.
        transforms={}
        for name,amount in errors.items():
            if not amount:continue
            d=self.byname[name];mode=d['mode']
            if 'group' in d:
                group=d['group'];entry=transforms.setdefault(group,dict(t=np.zeros(3),r=np.zeros(3)))
                if mode in ['x','y','z']:entry['t'][['x','y','z'].index(mode)]+=amount
                elif mode in ['tx','ty']:entry['r'][['tx','ty'].index(mode)]+=amount
                else:
                    i=self.groups[group][0];ap=self.nom.surfaces[i].aperture;g=self.nom.surfaces[i].geometry
                    y=ap.offset_y;eps=1e-4;slope=(sag(y+eps,float(g.radius),float(g.k))-sag(y-eps,float(g.radius),float(g.k)))/(2*eps)
                    normal=np.array([0,-slope,1]);entry['r']+=amount*normal/np.linalg.norm(normal)
            else:
                i=d['surface'];g=o.surfaces[i].geometry
                if mode=='radius':g.radius=g.radius*(1+amount)
                elif mode=='conic':g.k=g.k+amount
                elif mode=='thickness':o.surfaces[i+1].geometry.cs.z+=amount
                elif mode=='index':
                    mat=copy.copy(o.surfaces[i].material_post);base=mat.n
                    mat.n=lambda wavelength,_base=base,_delta=amount,**kw:_base(wavelength,**kw)+_delta
                    o.surfaces[i].material_post=mat
        for group,tr in transforms.items():
            ids=self.groups[group];i=ids[0];g=self.nom.surfaces[i].geometry
            p=np.array([0.,0.,float(g.cs.z)])
            if self.b06 and group!='detector':
                ap=self.nom.surfaces[i].aperture;p[:2]=[ap.offset_x,ap.offset_y];p[2]+=sag(np.hypot(*p[:2]),float(g.radius),float(g.k))
            rot=Rotation.from_rotvec(tr['r']);R=rot.as_matrix();angles=rot.as_euler('xyz')
            for idx in ids:
                cs=o.surfaces[idx].geometry.cs;v=np.array([float(cs.x),float(cs.y),float(cs.z)])
                v=p+R@(v-p)+tr['t'];cs.x,cs.y,cs.z=v;cs.rx,cs.ry,cs.rz=angles
            # B05 return primary hole moves with its parent mirror.
            if group=='primary' and not self.b06:
                o.surfaces[4].geometry.cs=copy.deepcopy(o.surfaces[2].geometry.cs)
        return o

    def pupil(self,n=5):
        # Same equal-area coordinates and azimuth samples in each physical pupil.
        inner=0 if self.b06 else A.AP['obstruction']/(D/2)
        r=np.sqrt(inner**2+(1-inner**2)*(np.arange(n)+.5)/n)
        t=(np.arange(4*n)+.5)*2*np.pi/(4*n)
        x=(r[:,None]*np.cos(t)).ravel();y=(r[:,None]*np.sin(t)).ravel()
        if self.b06:x=x*D/self.parentD;y=(y*D+2*S['seed']['offset'])/self.parentD
        return x,y

    def sample(self,errors={},n=4,waves=WAVES,fields=FIELDS):
        o=self.build(errors);px,py=self.pupil(n);pts=[];alive=[];history=[]
        for field in fields:
            colors=[];keeps=[]
            for wl in waves:
                r=o.ray_tracer.trace_generic(*field,px,py,wl)
                p=np.column_stack([r.x,r.y,r.z]);cs=o.surfaces[-1].geometry.cs
                origin,rot=cs.get_effective_transform();local=(p-np.asarray(origin))@np.asarray(rot)
                colors.append(local[:,:2]);keeps.append((np.asarray(r.i)>0)&np.isfinite(local).all(axis=1))
                if wl==.55:history.append((np.array(o.surfaces.x),np.array(o.surfaces.y),np.array(o.surfaces.z)))
            pts.append(colors);alive.append(keeps)
        pts=np.array(pts);alive=np.array(alive);center=np.mean(pts,axis=(1,2),keepdims=True)
        residual=pts-center
        if not np.isfinite(residual).all():raise ValueError('Nonfinite rays; do not disguise as a sensitivity')
        rms=np.sqrt(np.mean(np.sum(residual**2,axis=-1),axis=2))*1000
        result=dict(worst_rms_um=float(rms.max()),median_rms_um=float(np.median(rms)),p90_rms_um=float(np.percentile(rms,90)),
            rms_by_field_wavelength_um=rms.tolist(),centroids_mm=center[:,0,0,:].tolist(),minimum_survival=float(alive.mean(axis=2).min()),
            survival_by_field_wavelength=alive.mean(axis=2).tolist())
        return residual.ravel(),result,history

    def scale(self,errors={}):
        eps=1e-4;fields=[(eps,0),(-eps,0),(0,eps),(0,-eps)]
        _,met,_=self.sample(errors,4,[.55],fields);c=np.array(met['centroids_mm'])
        j=np.column_stack([(c[0]-c[1]),(c[2]-c[3])])/(2*eps*np.radians(A.ANG))
        return dict(jacobian_mm_per_radian=j.tolist(),axis_scales_mm=np.linalg.norm(j,axis=0).tolist())

    def diffraction(self,errors,field,wl,physical_n=112):
        o=self.build(errors);n=int(round(physical_n*self.parentD/D));pad=4
        ps=ScalarFFTPSF(o,field,wl,num_rays=n,grid_size=n*pad,strategy='centroid_sphere',remove_tilt=False,robust_trim_std=0)
        data=ps.get_data(field,wl);phase=np.asarray(data.opd);amp=np.sqrt(np.asarray(data.intensity));ok=amp>0
        assert np.all(np.isfinite(phase[ok]))
        axis=np.linspace(-1,1,n);xx,yy=np.meshgrid(axis,axis);disk=xx*xx+yy*yy<=1
        p=np.zeros((n,n),complex);v=np.zeros_like(phase,dtype=complex);v[ok]=amp[ok]*np.exp(-2j*np.pi*phase[ok]);p[disk]=v
        dx=wl*1e-3*F/self.parentD*(n-1)/(n*pad);size=n*pad;mid=size//2
        freqs=np.fft.fftshift(np.fft.fftfreq(size,d=dx));coord=(np.arange(size)-mid)*dx;half=A.R['pixel_pitch_um'][0]/1000
        weights=np.maximum(0,np.minimum(coord+dx/2,half)-np.maximum(coord-dx/2,-half))/dx
        def calc(pupil):
            im=abs(np.fft.fftshift(np.fft.fft2(pupil,s=(size,size))))**2;im/=im.sum()
            otf=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(im)));otf/=otf[mid,mid]
            return dict(mtf_x=np.interp(FREQ,freqs[mid:],abs(otf[mid,mid:])).tolist(),
                mtf_y=np.interp(FREQ,freqs[mid:],abs(otf[mid:,mid])).tolist(),ee2=float(weights@im@weights))
        return dict(field=field,wavelength_um=wl,physical_pupil_sampling=physical_n,parent_grid=n,actual=calc(p),matched=calc(abs(p)))

def run(cid):
    c=Candidate(cid);folder=Path(cid);start=time.monotonic()
    if (OUT/folder/'sensitivity.json').exists():print(cid,'sensitivity checkpoint retained',flush=True);return
    r0,base,_=c.sample();jac=[];rows=[]
    # Finite central differences, not a nominal optimization.
    for d in c.defs:
        name=d['name'];h=d['step'];rm,mm,_=c.sample({name:-h});rp,mp,_=c.sample({name:h})
        column=(rp-rm)/2;jac.append(column)
        rows.append(dict(**d,minus=mm,plus=mp,residual_slope_um_per_unit=float(np.sqrt(np.mean(((rp-rm)/(2*h))**2))*1000),
            nonlinearity_fraction=float(np.linalg.norm((rp+rm)/2-r0)/max(np.linalg.norm(column),1e-15)),
            image_scale_plus=c.scale({name:h})))
    J=np.column_stack(jac);np.savez(OUT/folder/'jacobian.npz',J=J,nominal=r0)
    names=[d['name'] for d in c.defs]
    sets={'focus':['detector_z'],'focus_secondary_tilt':['detector_z','secondary_tx','secondary_ty'],
          'focus_secondary_z':['detector_z','secondary_z'],
          'focus_detector_tilt':['detector_z','detector_tx','detector_ty']}
    if not c.b06:sets['focus_corrector_z']=['detector_z','corrector_z']
    else:sets['focus_tertiary_tilt']=['detector_z','tertiary_tx','tertiary_ty']
    coupling={}
    for label,ns in sets.items():
        C=J[:,[names.index(n) for n in ns]];norms=np.linalg.norm(C,axis=0);sv=np.linalg.svd(C/np.maximum(norms,1e-20),compute_uv=False)
        coupling[label]=dict(names=ns,normalized_condition=float(sv[0]/max(sv[-1],1e-20)),
            correlation=((C.T@C)/np.outer(norms,norms)).tolist())
    # One linear least-squares correction per case, centered on nominal residual.
    # Limits: 0.5 mm axial, 1 mrad tilt. No free shape/index changes.
    def compensate(errors,residual,label):
        ns=sets[label];C=J[:,[names.index(n) for n in ns]]
        q=np.linalg.lstsq(C,-(residual-r0),rcond=1e-8)[0]
        amounts={n:float(np.clip(v*c.byname[n]['step'],-(.001 if 't' in n.split('_')[-1] else .5),(.001 if 't' in n.split('_')[-1] else .5))) for n,v in zip(ns,q)}
        total=errors.copy()
        for n,v in amounts.items():total[n]=total.get(n,0)+v
        rr,met,_=c.sample(total)
        return dict(adjustments=amounts,total_errors=total,metrics=met,
            linear_prediction_error_um=float(np.sqrt(np.mean((rr-(residual+C@q))**2))*1000))
    recovery=[]
    for row in rows:
        for sign in [-1,1]:
            errors={row['name']:sign*row['step']};rr,met,_=c.sample(errors)
            recovery.append(dict(error=errors,uncompensated=met,
                compensated={label:compensate(errors,rr,label) for label in ['focus','focus_secondary_tilt']}))
    save(folder/'sensitivity.json',dict(nominal=base,nominal_scale=c.scale(),definitions=c.defs,rows=rows,
        compensator_coupling=coupling,recovery=recovery,seconds=time.monotonic()-start))
    print(cid,'sensitivity done',base['worst_rms_um'],'seconds',time.monotonic()-start,flush=True)

def main():
    cid=sys.argv[1];(OUT/cid).mkdir(exist_ok=True)
    if '--probe' in sys.argv:
        c=Candidate(cid);print(json.dumps(c.sample()[1]));print(c.scale());print(c.sample({'secondary_tx':.0001})[1]['worst_rms_um']);return
    run(cid)

if __name__=='__main__':main()
