"""Matched uniform-temperature scenarios. Frozen shapes; no shape optimization."""
import sys, json, copy, time
from pathlib import Path
import numpy as np
import track_b_run010_sensitivity as M
OUT=M.ROOT/'runs/run_013'
SCENARIOS={'silica_high_frame':(.52,24), 'silica_low_frame':(.52,1.2),
           'homogeneous_high_CTE':(24,24)}
def save(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')

class Thermal(M.Candidate):
    def __init__(self,cid,T,mirror_ppm,frame_ppm,glass=True):
        super().__init__(cid)
        self.original_parent=self.parentD
        self.temperature=T
        dt=T-20; sm=1+mirror_ppm*1e-6*dt; ss=1+frame_ppm*1e-6*dt
        old=copy.deepcopy(self.nom)
        # Coordinate datum is the nominal entrance-plane parent origin.
        # Structural distances locate physical patch/lens centers; mirror
        # curvature, off-axis patch and clear apertures expand with substrate.
        for i,s in enumerate(self.nom.surfaces):
            if i==0:continue
            g=s.geometry; go=old.surfaces[i].geometry
            p=np.array([float(go.cs.x),float(go.cs.y),float(go.cs.z)])
            body=sm if i in ([2,3,4] if self.b06 else [2,3,4]) else ss
            if i in ([2,3,4] if self.b06 else [2,3]):
                ap=old.surfaces[i].aperture
                xy=np.array([getattr(ap,'offset_x',0),getattr(ap,'offset_y',0)])
                local=np.r_[xy,M.sag(np.linalg.norm(xy),float(go.radius),float(go.k))]
                p=ss*(p+local)-sm*local
            else:p=p*ss
            g.cs.x,g.cs.y,g.cs.z=p
            if np.isfinite(float(go.radius)):g.radius=go.radius*body
            ap=s.aperture
            for attr in ['r_max','r_min','offset_x','offset_y']:
                if hasattr(ap,attr):setattr(ap,attr,getattr(ap,attr)*body)
        if not self.b06:
            for front,alpha in [(5,7.1),(7,7.8)]:
                sg=1+alpha*1e-6*dt if glass else ss
                z0=float(old.surfaces[front].geometry.cs.z)
                z1=float(old.surfaces[front+1].geometry.cs.z)
                center=(z0+z1)/2*ss
                for idx,z in [(front,z0),(front+1,z1)]:
                    g=self.nom.surfaces[idx].geometry
                    g.cs.z=center+(z-(z0+z1)/2)*sg
                    g.radius=old.surfaces[idx].geometry.radius*sg
                    self.nom.surfaces[idx].aperture.r_max=old.surfaces[idx].aperture.r_max*sg
                if glass:
                    mat=copy.copy(self.nom.surfaces[front].material_post);base=mat.n
                    mat.n=lambda wl,_base=base,_T=T,**kw:_base(wl,temperature=_T,pressure=1)
                    self.nom.surfaces[front].material_post=mat
        self.parentD*=ss
        self.nom.set_aperture(aperture_type='EPD',value=self.parentD)
    def pupil(self,n=4):
        # Preserve normalized physical entrance sampling as its frame expands.
        current=self.parentD;self.parentD=self.original_parent
        result=super().pupil(n);self.parentD=current
        return result
    def build(self,errors={}):
        # The inherited nominal pivot assumes zero parent x/y. Thermal patch
        # expansion can move that origin, so use the actual physical patch.
        if not self.b06:return super().build(errors)
        o=copy.deepcopy(self.nom)
        assert set(errors)<=set(['detector_z','secondary_tx','secondary_ty'])
        o.surfaces[-1].geometry.cs.z+=errors.get('detector_z',0)
        g=o.surfaces[3].geometry;ap=o.surfaces[3].aperture
        v=np.array([float(g.cs.x),float(g.cs.y),float(g.cs.z)])
        local=np.array([ap.offset_x,ap.offset_y,M.sag(np.hypot(ap.offset_x,ap.offset_y),float(g.radius),float(g.k))])
        p=v+local
        rot=M.Rotation.from_rotvec([errors.get('secondary_tx',0),errors.get('secondary_ty',0),0])
        g.cs.x,g.cs.y,g.cs.z=p+rot.as_matrix()@(v-p)
        g.cs.rx,g.cs.ry,g.cs.rz=rot.as_euler('xyz')
        return o

def run(cid):
    path=OUT/(cid+'.json')
    if path.exists():print(cid,'checkpoint retained',flush=True);return
    start=time.monotonic();base=M.Candidate(cid);r0,met0,_=base.sample()
    zero=Thermal(cid,20,.52,24);rz,_,_=zero.sample()
    assert np.max(abs(rz-r0))<1e-10, '20 C reconstruction failed'
    # Exact geometric homology with thermo-optic change disabled is a model check.
    hom=Thermal(cid,50,24,24,glass=False);rh,mh,_=hom.sample()
    homerr=float(np.max(abs(rh-r0*(1+24e-6*30))))
    assert homerr<1e-8, ('homology failed',homerr)
    archive=np.load(M.ROOT/f'runs/run_010/{cid}/jacobian.npz')
    J=archive['J'];assert np.max(abs(archive['nominal']-r0))<1e-10
    names=[d['name'] for d in base.defs];rows=[]
    for scenario,(am,af) in SCENARIOS.items():
        for T in [-25,-10,20,35,50]:
            c=Thermal(cid,T,am,af);r,met,_=c.sample()
            row=dict(scenario=scenario,temperature_C=T,uncompensated=met,compensated={})
            for label,ns in [('focus',['detector_z']),('focus_secondary_tilt',['detector_z','secondary_tx','secondary_ty'])]:
                C=J[:,[names.index(n) for n in ns]]
                q=np.linalg.lstsq(C,-(r-r0),rcond=1e-8)[0]
                raw={n:float(v*base.byname[n]['step']) for n,v in zip(ns,q)}
                adj={n:float(np.clip(v,-(.5 if n=='detector_z' else .001),(.5 if n=='detector_z' else .001))) for n,v in raw.items()}
                rc,mc,_=c.sample(adj)
                row['compensated'][label]=dict(adjustments=adj,unbounded_adjustments=raw,cap_hit=any(abs(adj[n]-raw[n])>1e-12 for n in ns),metrics=mc,image_scale=c.scale(adj))
            rows.append(row)
            save(cid+'_checkpoint.json',dict(rows=rows))
            print(cid,scenario,T,'RMS',round(met['worst_rms_um'],3),'focus',round(row['compensated']['focus']['metrics']['worst_rms_um'],3),'3ctrl',round(row['compensated']['focus_secondary_tilt']['metrics']['worst_rms_um'],3),flush=True)
    save(cid+'.json',dict(candidate=cid,nominal=met0,zero_temperature_max_residual_error_mm=float(np.max(abs(rz-r0))),homology_max_error_mm=homerr,rows=rows,seconds=time.monotonic()-start))

if __name__=='__main__':run(sys.argv[1])
