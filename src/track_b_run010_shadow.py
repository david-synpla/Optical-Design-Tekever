"""Direct nonincident B05 secondary interception check at the pupil inner rim."""
import sys,json
from pathlib import Path
import numpy as np
from optiland.rays import RealRays
import track_b_run010_sensitivity as m

def run(cid):
    c=m.Candidate(cid);lhs=m.read(Path(cid)/'lhs.json');idx=lhs['summary']['focus_secondary_tilt']['worst_case'];case=m.read(Path(cid)/'lhs'/f'{idx:03}.json')
    out={}
    for label,errors in [('nominal',{}),('compensated_specimen',case['compensated']['focus_secondary_tilt']['total_errors'])]:
        o=c.build(errors);rows=[]
        for density in [64,128]:
            rin=35.5;rout=35.6;r=np.sqrt(rin**2+(rout**2-rin**2)*(np.arange(density)+.5)/density)
            theta=(np.arange(1024)+.5)*2*np.pi/1024;x=(r[:,None]*np.cos(theta)).ravel();y=(r[:,None]*np.sin(theta)).ravel()
            values=[]
            for field in m.FIELDS:
                px,py=c.pupil(2);o.ray_tracer.trace_generic(*field,px,py,.55);stop=o.surfaces[1]
                incoming=RealRays(x,y,np.zeros_like(x),np.full_like(x,float(stop.L[0])),np.full_like(x,float(stop.M[0])),np.full_like(x,float(stop.N[0])),np.ones_like(x),.55)
                g=o.surfaces[3].geometry;g.localize(incoming);t=g.distance(incoming)
                radius=np.hypot(incoming.x+t*incoming.L,incoming.y+t*incoming.M)
                hit=(radius<=35.5)&(t>0);fraction=float(hit.mean()*(rout**2-rin**2)/((m.D/2)**2-rin**2))
                # Outermost quadrature ring must be clear to bound the thin-shell integration.
                assert not hit.reshape(density,1024)[-1].any()
                values.append(dict(field=field,additional_blocked_fraction_of_annulus=fraction))
            rows.append(dict(radial_samples=density,azimuth_samples=1024,rows=values))
        out[label]=rows
    m.save(Path(cid)/'secondary_shadow.json',dict(results=out,note='Direct intersection of incoming rays with the saved/rigidly moved secondary optical patch. Thin-shell equal-area integral; excludes unknown substrate and spider. Original annular models remain unchanged.'))
    print(cid,json.dumps({key:max(r['additional_blocked_fraction_of_annulus'] for r in rows[-1]['rows']) for key,rows in out.items()}),flush=True)

if __name__=='__main__':run(sys.argv[1])
