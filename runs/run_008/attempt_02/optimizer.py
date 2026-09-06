"""B05 second distinct attempt: cap secondary asphere at K=-6 (benchmark choice).
Keeps first result immutable; saves new attempt_02 directory.
"""
import json, time, shutil, hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
import track_b_run008_cassegrain as m

out=m.ROOT/'runs/run_008/attempt_02'; out.mkdir(exist_ok=False)
config=json.loads((m.ROOT/'runs/run_008/configuration.json').read_text())
x=np.array(config['best']); x[10]=-5.99
lo=np.array(config['bounds'][0]); hi=np.array(config['bounds'][1]); lo[10]=-6
start=time.monotonic()
fit=least_squares(m.merit,x,bounds=(lo,hi),x_scale='jac',max_nfev=70,ftol=1e-5,xtol=1e-6,gtol=1e-5)
metrics=m.geometric(fit.x)
(out/'configuration.json').write_text(json.dumps(dict(best=fit.x.tolist(),initial=x.tolist(),bounds=[lo.tolist(),hi.tolist()],
    rationale='Test a less aspheric secondary; K is a screening proxy, actual departure/slope/metrology must decide'),indent=2)+'\n')
(out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
rows=[]
for field in [(0,0),(m.HX,m.HY)]:
    for wl in m.WAVES:rows.append(m.diffraction(fit.x,field,wl))
(out/'diffraction.json').write_text(json.dumps(rows,indent=2)+'\n')
(out/'metadata.json').write_text(json.dumps(dict(track='B',candidate='B05',run='008',attempt=2,
    substantial_search_count=1,nfev=fit.nfev,message=fit.message,seconds=time.monotonic()-start,
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
shutil.copy2(__file__,out/'optimizer.py')
print(json.dumps(dict(worst_rms_um=metrics['worst_rms_um'],parameters=fit.x.tolist(),seconds=time.monotonic()-start),indent=2))
