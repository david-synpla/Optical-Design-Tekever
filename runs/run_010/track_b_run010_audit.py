"""Independent denser/boundary checks and compact report tables; no searches."""
import sys,json,csv,copy,hashlib,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import track_b_run010_sensitivity as m
from track_b_run010_interfaces import clearance

def run(cid):
    c=m.Candidate(cid);folder=Path(cid);sen=m.read(folder/'sensitivity.json');lhs=m.read(folder/'lhs.json')
    idx=lhs['summary']['focus_secondary_tilt']['worst_case'];case=m.read(folder/'lhs'/f'{idx:03}.json');errors=case['compensated']['focus_secondary_tilt']['total_errors']
    fields=[(x*m.A.HX,y*m.A.HY) for x in np.linspace(-1,1,5) for y in np.linspace(-1,1,5)]
    dense={}
    for label,e in [('nominal',{}),('compensated_specimen',errors)]:dense[label]=c.sample(e,12,fields=fields)[1]
    comparisons=[]
    for fine in m.read(folder/'diffraction_convergence.json'):
        coarse=next(r for r in m.read(folder/f'diffraction_{fine["scenario"]}.json')['rows'] if np.allclose(r['field'],fine['field']) and r['wavelength_um']==fine['wavelength_um'])
        comparisons.append(dict(scenario=fine['scenario'],wavelength_um=fine['wavelength_um'],
            max_mtf_difference=max(float(np.max(abs(np.array(fine['actual'][key])-coarse['actual'][key]))) for key in ['mtf_x','mtf_y']),
            ee2_difference=abs(fine['actual']['ee2']-coarse['actual']['ee2'])))
    # Ring extrema matter for clearance; area quadrature is not a boundary audit.
    def boundary(n):
        r0=0 if c.b06 else m.A.AP['obstruction']/(m.D/2)
        r=np.array([r0+1e-8,1-1e-8]);th=np.linspace(0,2*np.pi,256,endpoint=False)
        x=(r[:,None]*np.cos(th)).ravel();y=(r[:,None]*np.sin(th)).ravel()
        if c.b06:x=x*m.D/c.parentD;y=(y*m.D+2*m.S['seed']['offset'])/c.parentD
        return x,y
    cb=m.Candidate(cid);cb.pupil=boundary
    boundary_checks={label:clearance(cb,e) for label,e in [('nominal',{}),('compensated_specimen',errors)]}
    scale_rows=[];travel=[];nonlinear=[];saturated={key:0 for key in lhs['summary'] if key!='uncompensated'}
    for i in range(24):
        q=m.read(folder/'lhs'/f'{i:03}.json');cc=q['compensated']['focus_secondary_tilt'];scale_rows.append(c.scale(cc['total_errors']))
        travel.append(cc['adjustments']);nonlinear.append(q['linear_prediction_error_um'])
        for key in saturated:saturated[key]+=bool(q['compensated'][key]['saturated'])
    surface_steps=[]
    for d in c.defs:
        if d['mode'] not in ['radius','conic']:continue
        i=d['surface'];g=c.nom.surfaces[i].geometry;ap=c.nom.surfaces[i].aperture
        rad=float(ap.r_max);y0=float(getattr(ap,'offset_y',0));theta=np.linspace(0,2*np.pi,64,endpoint=False);rr=np.sqrt((np.arange(16)+.5)/16)*rad
        xx=(rr[:,None]*np.cos(theta)).ravel();yy=(y0+rr[:,None]*np.sin(theta)).ravel();r=np.hypot(xx,yy)
        R=float(g.radius);k=float(getattr(g,'k',0));a=m.sag(r,R,k);b=m.sag(r,R*(1+d['step']) if d['mode']=='radius' else R,k+d['step'] if d['mode']=='conic' else k)
        delta=b-a;P=np.column_stack([np.ones(len(xx)),xx,yy]);res=delta-P@np.linalg.lstsq(P,delta,rcond=None)[0]
        surface_steps.append(dict(parameter=d['name'],step=d['step'],sag_rms_after_piston_tilt_um=float(np.sqrt(np.mean(res**2))*1000),
            max_raw_sag_change_um=float(max(abs(delta))*1000),note='Axial sag difference, not normal figure error or supplier tolerance; radius/power remains included'))
    audit=dict(dense_25field_576ray=dense,diffraction_convergence=comparisons,boundary_clearance=boundary_checks,
        compensated_lhs_image_scales=scale_rows,compensator_travel=travel,saturated_case_counts=saturated,
        max_uncompensated_linear_prediction_error_um=max(nonlinear),surface_diagnostic_sag=surface_steps)
    m.save(folder/'audit.json',audit)
    with (m.OUT/folder/'sensitivity.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['parameter','diagnostic_step','unit','minus_worst_RMS_um','plus_worst_RMS_um','ray_coordinate_slope_um_per_unit','nonlinearity_fraction','plus_focus_RMS_um','plus_3comp_RMS_um'])
        for row in sen['rows']:
            rec=next(r for r in sen['recovery'] if r['error'].get(row['name'])==row['step'])
            writer.writerow([row['name'],row['step'],row['unit'],row['minus']['worst_rms_um'],row['plus']['worst_rms_um'],row['residual_slope_um_per_unit'],row['nonlinearity_fraction'],rec['compensated']['focus']['metrics']['worst_rms_um'],rec['compensated']['focus_secondary_tilt']['metrics']['worst_rms_um']])
    print(cid,json.dumps(dict(dense={k:v['worst_rms_um'] for k,v in dense.items()},convergence=comparisons,boundary=boundary_checks,
        max_nonlinearity=max(nonlinear),saturated=saturated)),flush=True)

def plots():
    ids=['B05-1','B05-2','B06'];labels=['uncompensated','focus','focus_secondary_tilt'];colors=['tab:blue','tab:orange','tab:green']
    fig,ax=plt.subplots(figsize=(9,4))
    for j,cid in enumerate(ids):
        rows=[m.read(Path(cid)/'lhs'/f'{i:03}.json') for i in range(24)]
        vals=[[r['uncompensated']['worst_rms_um'] if label=='uncompensated' else r['compensated'][label]['metrics']['worst_rms_um'] for r in rows] for label in labels]
        for k,v in enumerate(vals):ax.scatter(np.full(24,k+(j-1)*.22),v,s=12,alpha=.6,color=colors[j],label=cid if k==0 else None)
    ax.set_xticks(range(3),['No compensation','Detector focus','Focus + secondary X/Y tilt']);ax.set_ylabel('Worst 9-field / 6-color RMS (um)');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(m.OUT/'coupled_errors.png',dpi=150)
    fig,axs=plt.subplots(1,3,figsize=(12,4),sharey=True)
    for ax,wl in zip(axs,[.43,.55,.8]):
        for cid,color in zip(ids,colors):
            data=m.read(Path(cid)/'diffraction_focus_secondary_tilt.json');row=next(r for r in data['rows'] if r['field'][0]>0 and r['field'][1]>0 and r['wavelength_um']==wl)
            ax.plot(m.FREQ,row['actual']['mtf_x'],'o-',color=color,label=cid+' X');ax.plot(m.FREQ,row['actual']['mtf_y'],'s--',color=color,label=cid+' Y')
        ax.set(title=f'{wl*1000:g} nm',xlabel='Spatial frequency (lp/mm)',ylim=(0,.85));ax.grid(alpha=.2)
    axs[0].set_ylabel('Compensated specimen corner MTF');axs[0].legend(fontsize=7);fig.suptitle('Worst sampled RMS specimen after 3 compensators; not worst spectral MTF or yield');fig.tight_layout();fig.savefig(m.OUT/'compensated_mtf.png',dpi=150)

if __name__=='__main__':
    if sys.argv[1]=='plots':plots()
    else:run(sys.argv[1])
