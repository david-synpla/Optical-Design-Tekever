"""Small assembly diagnostics, not supplier tolerances or yield prediction."""
import json,copy
import numpy as np
import track_b_run012_newtonian as M
def main():
    x=json.loads((M.OUT/'attempt_01.json').read_text())['parameters'];px,py=M.pupil(10)
    def sample(case=None,amount=0,focus=0):
        o=M.build(x,folded=True)
        if case=='primary_radius':o.surfaces[2].geometry.radius*=1+amount
        if case=='flat_tilt':o.surfaces[3].geometry.cs.ry+=amount
        if case=='lens1_decenter':
            for i in [4,5]:o.surfaces[i].geometry.cs.y+=amount
        o.surfaces[8].geometry.cs.x+=focus
        residual=[];rms=[];survival=[];centers=[]
        for field in M.FIELDS:
            o.surfaces[1].aperture.set_field(*field);points=[];masks=[]
            for wl in M.WAVES:
                r=o.ray_tracer.trace_generic(*field,px,py,wl);points.append(np.column_stack([-r.z,r.y]));masks.append(r.i>0)
            p=np.array(points);k=np.array(masks);center=p[k].mean(axis=0);centers.append(center.tolist())
            e=p-center;residual.extend(e[k].ravel());rms.extend([float(np.sqrt(np.mean(np.sum(a[b]**2,axis=1)))*1000) for a,b in zip(e,k)]);survival.extend(k.mean(axis=1).tolist())
        return np.array(residual),dict(worst_rms_um=max(rms),minimum_survival=min(survival),centroids_mm=centers)
    r0,nom=sample();rows=[]
    for case,step,unit in [('primary_radius',.001,'fractional radius'),('flat_tilt',.0001,'rad'),('lens1_decenter',.01,'mm')]:
        for sign in [-1,1]:
            amount=sign*step;r,initial=sample(case,amount);focus=0
            assert len(r)==len(r0),'Clipping changes residual membership; stop this diagnostic'
            for _ in range(2):
                r=sample(case,amount,focus)[0]
                col=(sample(case,amount,focus+.01)[0]-sample(case,amount,focus-.01)[0])/.02
                focus+=float(col@(r0-r)/(col@col));focus=float(np.clip(focus,-2,2))
            _,final=sample(case,amount,focus)
            rows.append(dict(case=case,amount=amount,unit=unit,uncompensated=initial,focus_mm=focus,compensated=final))
    M.save('sensitivity.json',dict(nominal=nom,rows=rows,note='Six one-at-a-time diagnostic cases; two linear focus corrections capped at +/-2 mm; not a tolerance allocation. Centered RMS does not include pointing/registration.'))
    print([(r['case'],r['amount'],r['uncompensated']['worst_rms_um'],r['compensated']['worst_rms_um'],r['focus_mm']) for r in rows])
if __name__=='__main__':main()
