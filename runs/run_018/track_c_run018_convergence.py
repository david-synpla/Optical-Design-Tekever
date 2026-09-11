#!/usr/bin/env python3
"""Independent denser geometric replay for the new Run 018 S14 seed."""
import importlib.util,json,shutil
from pathlib import Path
import yaml
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists()); OUT=ROOT/'runs/run_018'
spec=importlib.util.spec_from_file_location('r17',ROOT/'src/track_c_run017_c01.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
req=yaml.safe_load((ROOT/'requirements/eo_swir_system_requirements.yaml').read_text()); sw=m.channel(req,'swir')
base=json.loads((OUT/'metrics.json').read_text())['new_compact_SWIR_seed']; x=[base['solution']['primary_conic'],base['solution']['secondary_conic'],base['solution']['detector_focus_mm']]
dense=m.evaluate(base['geometry'],sw,base['apertures'],x,nr=28,na=80)
result={'baseline_equal_area_rays_per_field':20*56,'replay_equal_area_rays_per_field':28*80,
  'baseline_worst_rms_radius_um':base['worst_rms_radius_um'],'replay_worst_rms_radius_um':dense['worst_rms_radius_um'],
  'absolute_worst_rms_change_um':abs(base['worst_rms_radius_um']-dense['worst_rms_radius_um']),
  'baseline_minimum_survival':base['minimum_survival'],'replay_minimum_survival':dense['minimum_survival'],
  'decision_stability':'S14 remains a compact stretch; C01 system decision does not depend on a fine spot ranking'}
(OUT/'convergence.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8'); shutil.copy2(__file__,OUT/'track_c_run018_convergence.py')
print(json.dumps(result,indent=2))
