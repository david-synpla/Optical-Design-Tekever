"""Finite range, material provenance, sampling and boundary-clearance checks."""
import json,hashlib
import numpy as np
import track_b_run013_thermal as T
import track_b_run010_interfaces as I
M=T.M
def main():
    materials=[]
    for idx in [5,7]:
        mat=M.Candidate('B05-1').nom.surfaces[idx].material_post
        materials.append(dict(name=mat.name,catalog_file=mat.material_data['filename'],sha256=hashlib.sha256(open(mat.filename,'rb').read()).hexdigest(),thermal_coefficients=np.asarray(mat.thermdispcoef).ravel().tolist(),reference_temperature_C=mat._t0,index_table=[dict(temperature_C=temp,indices=[float(np.asarray(mat.n(w,temperature=temp,pressure=1)).item()) for w in M.WAVES]) for temp in [-25,20,50]]))
    T.save('glass_provenance.json',dict(wavelengths_um=M.WAVES,pressure_atm=1,materials=materials))
    results=[]
    for cid in ['B05-1','B05-2','B06']:
        data=json.loads((T.OUT/(cid+'_verification.json')).read_text())
        row=next(r for r in data['rows'] if r['scenario']=='silica_low_frame' and r['temperature_C']==-25)
        c=T.Thermal(cid,-25,*T.SCENARIOS['silica_low_frame']);adj=row['iterations'][-1]['applied'].copy()
        target,_,_=c.sample(adj)
        c.nom.surfaces[0].geometry.cs.z=-800000
        extra=0
        for _ in range(2):
            r,_,_=c.sample(adj);lo=adj.copy();hi=adj.copy();lo['detector_z']-=.01;hi['detector_z']+=.01
            col=(c.sample(hi)[0]-c.sample(lo)[0])/.02
            delta=float(col@(target-r)/(col@col));extra+=delta;adj['detector_z']+=delta
        finite=c.sample(adj,n=12)[1]
        c=T.Thermal(cid,-25,*T.SCENARIOS['silica_low_frame']);infadj=row['iterations'][-1]['applied']
        convergence=c.diffraction(infadj,(M.A.HX,M.A.HY),.55,160)
        # Same nominal-frequency convention as Run010; actual scale is reported
        # alongside it so it is not mistaken for fixed detector registration.
        original=next(d for d in row['diffraction'] if d['wavelength_um']==.55 and d['field'][0]!=0)
        error=max(abs(np.array(original['actual'][key])-np.array(convergence['actual'][key])).max() for key in ['mtf_x','mtf_y','ee2'])
        result=dict(candidate=cid,finite_800m_at_cold_low_frame=dict(extra_detector_z_mm=extra,total_adjustment=adj,metrics=finite),diffraction_convergence=convergence,max_mtf_or_ee_sampling_change=float(error))
        hotrow=next(r for r in data['rows'] if r['scenario']=='silica_low_frame' and r['temperature_C']==50)
        hot=T.Thermal(cid,50,*T.SCENARIOS['silica_low_frame']);ha=hotrow['iterations'][-1]['applied'].copy()
        ht=hot.sample(ha)[0];hot.nom.surfaces[0].geometry.cs.z=-800000;he=0
        for _ in range(2):
            r=hot.sample(ha)[0];lo=ha.copy();hi=ha.copy();lo['detector_z']-=.01;hi['detector_z']+=.01
            col=(hot.sample(hi)[0]-hot.sample(lo)[0])/.02
            delta=float(col@(ht-r)/(col@col));he+=delta;ha['detector_z']+=delta
        result['finite_800m_at_hot_low_frame']=dict(extra_detector_z_mm=he,total_adjustment=ha,metrics=hot.sample(ha,n=12)[1])
        if cid=='B06':
            # Include entrance boundary, not only interior quadrature.
            normal=c.pupil
            def boundary(n):
                px,py=normal(n);theta=np.arange(256)*2*np.pi/256
                # Infinitesimal inset avoids binary roundoff on exact hard edge.
                return np.r_[px,np.cos(theta)*M.D*(1-1e-9)/c.original_parent],np.r_[py,(np.sin(theta)*M.D*(1-1e-9)+2*M.S['seed']['offset'])/c.original_parent]
            c.pupil=boundary
            result['cold_boundary_clearance']=I.clearance(c,infadj)
        results.append(result);print(cid,'finite RMS',finite['worst_rms_um'],'extra travel',extra,'FFTchange',error,flush=True)
    T.save('interface_verification.json',dict(results=results))
if __name__=='__main__':main()
