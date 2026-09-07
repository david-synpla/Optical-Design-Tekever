"""Verify saved B09 geometry; no additional shape solve."""
import json,time,shutil,hashlib
import numpy as np
import track_b_run012_newtonian as M
def main():
    start=time.monotonic();x=json.loads((M.OUT/'attempt_01.json').read_text())['parameters']
    fields=[(a*M.HX,b*M.HY) for a in np.linspace(-1,1,5) for b in np.linspace(-1,1,5)]
    dense=M.geometric(x,n=24,fields=fields);M.save('dense.json',dense)
    fold_errors=[];u=M.build(x);o=M.build(x,folded=True);px,py=M.pupil(24)
    for f in M.FIELDS:
        for wl in M.WAVES:
            for a in [u,o]:a.surfaces[1].aperture.set_field(*f)
            r=u.ray_tracer.trace_generic(*f,px,py,wl);s=o.ray_tracer.trace_generic(*f,px,py,wl)
            live=(r.i>0)&(s.i>0);zf=float(o.surfaces[3].geometry.cs.z)
            err=max(np.max(abs(s.z[live]-(zf-r.x[live]))),np.max(abs(s.y[live]-r.y[live])))
            fold_errors.append(dict(field=f,wavelength_um=wl,max_coordinate_error_mm=float(err),unfolded_survival=float(np.mean(r.i>0)),folded_survival=float(np.mean(s.i>0)),different_survival_count=int(np.sum((r.i>0)!=(s.i>0)))))
    assert max(r['max_coordinate_error_mm'] for r in fold_errors)<1e-9
    M.save('physical_fold.json',dict(rows=fold_errors,correction='Set actual reflection flag; archived solve used unfolded model and its geometry is unchanged.'))
    # Separate intentionally obscured source area from additional clipping.
    clipping=[]
    for f in M.FIELDS:
        o=M.build(x,folded=True);o.surfaces[1].aperture.set_field(*f)
        # Stop is 0.01 mm ahead of primary; replay actual entrance history.
        r=o.ray_tracer.trace_generic(*f,px,py,.55)
        expected=o.surfaces[1].aperture.contains(np.asarray(o.surfaces.x)[1],np.asarray(o.surfaces.y)[1])
        clipping.append(dict(field=f,entrance_fraction=float(np.mean(expected)),additional_clipping_fraction_of_clear_pupil=float(np.sum(expected&(r.i<=0))/np.sum(expected))))
    M.save('clipping.json',dict(rows=clipping,pupil_samples=len(px)))
    opt=M.minimize_scalar(lambda df:M.geometric(x,focus=df,finite=True,n=8)['worst_rms_um'],bounds=(0,2),method='bounded',options={'maxiter':24,'xatol':1e-4})
    M.save('finite_800m.json',dict(extra_path_focus_mm=float(opt.x),optimizer_success=bool(opt.success),evaluations=opt.nfev,metrics=M.geometric(x,focus=opt.x,finite=True,n=24,fields=fields)))
    diff=[]
    for wl in [.43,.55,.8]:
        for field in [(0,0),(M.HX,M.HY),(-M.HX,-M.HY)]:
            d=M.diffraction(x,field,wl,n=384);diff.append(d);M.save('diffraction.json',dict(rows=diff,frequencies_lp_mm=M.FREQ.tolist()))
            print('diffraction',wl,field,d['actual'],flush=True)
    convergence=[]
    for field in [(0,0),(M.HX,M.HY)]:
        d=M.diffraction(x,field,.55,n=768);lo=next(v for v in diff if v['wavelength_um']==.55 and tuple(v['field'])==field)
        error=max(float(np.max(abs(np.array(d['actual'][k])-np.array(lo['actual'][k])))) for k in ['mtf_x','mtf_y','ee2'])
        convergence.append(dict(high=d,max_mtf_ee_change=error))
    M.save('diffraction_convergence.json',dict(rows=convergence))
    shutil.copy2(M.__file__,M.OUT/'verified_model.py');shutil.copy2(__file__,M.OUT/'verification.py')
    M.save('verification_metadata.json',dict(seconds=time.monotonic()-start,shape_optimization=False,finite_focus_optimizer_count=1,model_sha256=hashlib.sha256((M.OUT/'verified_model.py').read_bytes()).hexdigest()))
    print('DENSE',dense['worst_rms_um'],'finite',opt.x,'maxfold',max(r['max_coordinate_error_mm'] for r in fold_errors),'convergence',convergence[-1]['max_mtf_ee_change'],flush=True)
if __name__=='__main__':main()
