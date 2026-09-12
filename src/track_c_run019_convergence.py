#!/usr/bin/env python3
"""Dense pupil replay for the Run 019 C03 architecture screen."""
from __future__ import annotations
import json
from pathlib import Path
import track_c_run019_c03 as r19

OUT=r19.OUT

def main():
    req=r19.yaml.safe_load(r19.REQ.read_text(encoding='utf-8'))
    channels=[r19.channel(req,'eo'),r19.channel(req,'swir')]
    metrics=json.loads((OUT/'metrics.json').read_text(encoding='utf-8'))
    checks=[]
    for row in metrics['variants']:
        if row['geometry']['name'] not in ('A8_F1p0_O237','A4_F1p2_O289_R'):
            continue
        sol=row['solution']; ks=(sol['primary_conic'],sol['secondary_conic'])
        focuses=(sol['EO_focus_mm'],sol['SWIR_focus_mm'])
        item={'variant':row['geometry']['name'],'sampling':{'screen':[16,48],'dense':[24,72]},'channels':{}}
        for ci,c in enumerate(channels):
            o,ind=r19.build(row['geometry'],c,row['apertures'],focuses[ci],ks)
            traces=[r19.trace(o,ind,row['geometry'],c,f,w,24,72) for f in r19.fields(c) for w in c['waves_um']]
            dense=max(x['rms_radius_um'] for x in traces); screen=row['optical'][c['name']]['worst_rms_radius_um']
            item['channels'][c['name']]={'screen_worst_rms_um':screen,'dense_worst_rms_um':dense,
              'relative_change_percent':100*(dense-screen)/screen,'dense_minimum_survival':min(x['survival'] for x in traces)}
        checks.append(item)
    result={'purpose':'dense pupil replay of the compact-volume and best-nominal endpoints; not an added architecture attempt',
      'checks':checks,'pass_criterion':'absolute RMS replay change below 2%; physical survival at least 0.995 (finite quadrature versus 2 mm sizing margin)',
      'passed':all(abs(c['relative_change_percent'])<2 and c['dense_minimum_survival']>=.995 for i in checks for c in i['channels'].values())}
    r19.save('convergence.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
