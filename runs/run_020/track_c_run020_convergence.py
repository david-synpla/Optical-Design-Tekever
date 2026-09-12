#!/usr/bin/env python3
"""Dense replay and 800 m focus check for Run 020 retained optical point."""
from __future__ import annotations
import importlib.util,json
import numpy as np,yaml
from scipy.optimize import minimize_scalar
import track_c_run020_c04 as m

def load17():
    p=m.ROOT/'runs/run_017/track_c_run017_c01.py';s=importlib.util.spec_from_file_location('r17',p);q=importlib.util.module_from_spec(s);s.loader.exec_module(q);return q

def main():
    c=m.channel(yaml.safe_load(m.REQ.read_text(encoding='utf-8')));data=json.loads((m.OUT/'metrics.json').read_text(encoding='utf-8'))
    row=next(v for v in data['variants'] if v['geometry']['name']=='N1400_F63_L50');dense=m.evaluate(c,row['geometry'],row['parameters'],16,64)
    def finite_score(delta):
      x=np.array(row['parameters']);x[6]+=delta;o=m.build(c,row['geometry'],x,finite=True)
      traces=[m.trace(o,c,row['geometry'],f,w,7,28) for f in m.fields(c) for w in c['waves_um']]
      return max(t['rms_radius_um'] for t in traces)
    fit=minimize_scalar(finite_score,bounds=(0,8),method='bounded',options={'xatol':2e-4,'maxiter':45})
    derivatives=json.loads((m.OUT/'derivatives.json').read_text(encoding='utf-8'));cas=derivatives['attempt_4_stock_primary_custom_secondary'];r17=load17()
    cas_dense=r17.evaluate(cas['geometry'],c,cas['apertures'],[-1,cas['solution']['secondary_conic'],cas['solution']['detector_focus_mm']],24,64)
    out={'retained_newtonian_extender':{'variant':'N1400_F63_L50','screen_sampling':[10,40],'dense_sampling':[16,64],
      'screen_worst_rms_um':row['worst_rms_radius_um'],'dense_worst_rms_um':dense['worst_rms_radius_um'],
      'relative_change_percent':100*(dense['worst_rms_radius_um']/row['worst_rms_radius_um']-1),'dense_minimum_survival':dense['minimum_survival'],
      'infinity_to_800m_detector_refocus_mm':float(fit.x),'finite_800m_worst_rms_um':float(fit.fun),'focus_evaluations':int(fit.nfev)},
      'custom_secondary_derivative':{'screen_sampling':[18,48],'dense_sampling':[24,64],'screen_worst_rms_um':cas['worst_rms_radius_um'],
        'dense_worst_rms_um':cas_dense['worst_rms_radius_um'],'relative_change_percent':100*(cas_dense['worst_rms_radius_um']/cas['worst_rms_radius_um']-1),
        'dense_minimum_survival':cas_dense['minimum_survival']},
      'passed':abs(100*(dense['worst_rms_radius_um']/row['worst_rms_radius_um']-1))<2 and abs(100*(cas_dense['worst_rms_radius_um']/cas['worst_rms_radius_um']-1))<2}
    m.save('convergence.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':main()
