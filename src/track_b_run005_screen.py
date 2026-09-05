"""Independent requirements-derived Track B screening; no Track A imports/data.
Run with configured WSL Python. Output directory must not already exist.
"""
import sys, json, math, hashlib, shutil, platform
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import scipy
from scipy.special import j1
from scipy.integrate import simpson
import yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs/run_005'


def main():
    start = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(exist_ok=False)
    req = yaml.safe_load((ROOT/'requirements/eo_requirements.yaml').read_text())['source_explicit_requirements']
    p = req['pixel_pitch_um'][0] / 1000
    f = p / (req['instantaneous_fov_urad_per_pixel'] * 1e-6)
    n = req['f_number']; D = f/n
    width, height = np.array(req['array_px'])*p
    wavelengths = np.array([.43,.50,.55,.65,.725,.80])
    freqs = np.array([50.,100.,150.,1/(2*p)])
    tables = []
    # Airy PSF integral normalized analytically to unity over the infinite plane.
    # PSF density = pi/(4*(lambda*N)^2) * [2 J1(v)/v]^2.
    for wl in wavelengths:
        nu = freqs * wl * .001*n
        mtf = 2/np.pi*(np.arccos(nu)-nu*np.sqrt(1-nu**2))
        ee = []
        for pixels in [1,2,3]:
            a = pixels*p/2
            x = np.linspace(-a,a,401)
            xx,yy=np.meshgrid(x,x)
            v=np.pi*np.hypot(xx,yy)/(wl*.001*n)
            amp=np.ones_like(v); mask=v!=0
            amp[mask]=2*j1(v[mask])/v[mask]
            density=np.pi/(4*(wl*.001*n)**2)*amp**2
            ee.append(float(simpson(simpson(density,x=x,axis=1),x=x)))
        tables.append(dict(wavelength_um=float(wl),cutoff_lpmm=1/(wl*.001*n),
                           airy_diameter_um=2.44*wl*n,mtf=mtf.tolist(),ensquared_energy_1_2_3_pixels=ee))
    cots=[]
    for cid,name,efl,epd in [('B01','C5 + nominal 0.63 reducer',1250*.63,127),
                              ('B01-spacing','C5 tuned EFL (hypothesis)',f,127),
                              ('B02','Nikon nominal 800/6.3',800,800/6.3),
                              ('B09','130/650 Newtonian + target relay',f,130),
                              ('B14','Canon 800 stopped to nominal 6.2',800,800/6.2)]:
        cots.append(dict(id=cid,label=name,efl_mm=efl,epd_mm=epd,f_number=efl/epd,
                         ifov_urad=p/efl*1e6,efl_error_percent=100*(efl/f-1),
                         f_number_error_percent=100*((efl/epd)/n-1),
                         horizontal_fov_deg=math.degrees(2*math.atan(width/(2*efl))),
                         compliance='Nominal mismatch or unverified adjustment; no assumed customer tolerance'))
    metrics=dict(target=dict(efl_mm=f,epd_mm=D,f_number=n,active_width_mm=width,active_height_mm=height,
                  horizontal_fov_deg=math.degrees(2*math.atan(width/(2*f))),
                  vertical_fov_deg=math.degrees(2*math.atan(height/(2*f))),
                  thin_lens_800m_focus_shift_mm=f*f/(800000-f),nyquist_lpmm=1/(2*p)),
                 frequencies_lpmm=freqs.tolist(),clear_pupil_diffraction=tables,cots_first_order=cots,
                 assumptions=['Equal wavelength weights; no source/QE provided',
                              'Ideal clear circular pupil, incoherent imaging, no aberrations or obscuration',
                              'EE is optical energy in a centered square, before detector response',
                              '3x3 detector field grid is a screening sampling choice, not full verification'],
                 field_grid_deg=[[math.degrees(math.atan(x*width/(2*f))),math.degrees(math.atan(y*height/(2*f)))]
                                 for x in [-1,0,1] for y in [-1,0,1]])
    (OUT/'metrics.json').write_text(json.dumps(metrics,indent=2,allow_nan=False)+'\n')
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    for row in tables:
        ax[0].plot(freqs,row['mtf'],'o-',label=f"{row['wavelength_um']*1000:g} nm")
        ax[1].plot([1,2,3],row['ensquared_energy_1_2_3_pixels'],'o-')
    ax[0].set(xlabel='Spatial frequency (lp/mm)',ylabel='Ideal optical MTF',ylim=(0,1))
    ax[0].legend(fontsize=8)
    ax[1].set(xlabel='Centered square width (pixels)',ylabel='Ideal ensquared energy',ylim=(0,1),xticks=[1,2,3])
    fig.suptitle('f/6.2 clear-pupil diffraction reference — NOT candidate performance')
    fig.tight_layout(); fig.savefig(OUT/'diffraction_reference.png',dpi=150); plt.close(fig)
    shutil.copy2(__file__,OUT/'screen.py')
    shutil.copy2(ROOT/'requirements/eo_requirements.yaml',OUT/'requirements.yaml')
    metadata=dict(track='B',run_id='005',candidate_ids=[f'B{i:02d}' for i in range(1,15)],
                  stage='architecture screening',purpose='Identify branches worth development through a broad inexpensive comparison',
                  parent_run=None,track_a_seed_used=False,reference_accessed=False,
                  start_utc=start,end_utc=datetime.now(timezone.utc).isoformat(),
                  substantial_search_count=0,materially_distinct_optimizer_attempt_count=0,plateau=False,
                  stop_reason='Broad first-order/research gate answered; detailed optical performance remains unknown',
                  environment=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (OUT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metrics['target'],indent=2))
    print('Run 005 numerical screening saved. No optimizer invoked.')


if __name__ == '__main__':
    main()
