"""Verify closed-run data, capture provenance and archive reproducible scripts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess
import numpy as np
import track_b_run010_sensitivity as m

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=['runs/run_008/model.py','runs/run_008/configuration.json','runs/run_008/attempt_02/configuration.json',
        'runs/run_009/model.py','runs/run_009/attempt_01.json','requirements/eo_requirements.yaml',
        'DESIGN_WORKFLOW.md','OPTICAL_DESIGN_RULES.md','BENCHMARK_TRACKS.md','benchmark_protocol.md']
provenance={p:sha(m.ROOT/p) for p in inputs}
for folder in ['runs/run_008','runs/run_009']:
    meta=json.loads((m.ROOT/folder/'metadata.json').read_text(encoding='utf-8-sig'))
    assert sha(m.ROOT/folder/'model.py')==meta['script_sha256']
for line in (m.ROOT/'milestones/track_a_freeze/SHA256SUMS.txt').read_text().splitlines():
    expected,name=line.split('  ',1);assert sha(m.ROOT/'milestones/track_a_freeze'/name).lower()==expected.lower()
for cid in ['B05-1','B05-2','B06']:
    folder=Path(cid);s=m.read(folder/'sensitivity.json');a=m.read(folder/'audit.json')
    assert len(s['definitions'])==(29 if cid=='B06' else 38)
    assert len(list((m.OUT/folder/'lhs').glob('*.json')))==24
    assert m.read(folder/'interfaces.json')['nominal_replay_max_coordinate_difference_mm']==0
    assert a['saturated_case_counts']['focus_secondary_tilt']==0
    assert max(r['max_mtf_difference'] for r in a['diffraction_convergence'])<.003
    for label in ['nominal','uncompensated','focus','focus_secondary_tilt']:
        d=m.read(folder/f'diffraction_{label}.json');assert len(d['rows'])==9
        assert d['dense_metrics']['minimum_survival']==1
        for row in d['rows']:
            for key in ['actual','matched']:
                assert 0<=row[key]['ee2']<=1
                assert np.all((np.array(row[key]['mtf_x'])>=0)&(np.array(row[key]['mtf_x'])<=1))
    useful=[r['nonlinearity_fraction'] for r in s['rows'] if r['residual_slope_um_per_unit']*r['step']>.001]
    m.save(folder/'validation.json',dict(nominal_replay=True,selected_compensators_unsaturated=True,
        json_metric_ranges=True,convergence_pass=True,max_nonlinearity_for_responses_above_1nm=max(useful),
        note='Boundary/shadow limitations remain in audit.json and summary; finite field sampling is not certification.'))
for path in (m.ROOT/'src').glob('track_b_run010_*.py'):shutil.copy2(path,m.OUT/path.name)
shutil.copy2(m.ROOT/'requirements/eo_requirements.yaml',m.OUT/'requirements.yaml')
m.save('provenance.json',dict(base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=m.ROOT,text=True).strip(),
    input_sha256=provenance,track_a_freeze_hashes_pass=True,nominal_shape_changed=False,reference_accessed=False))
now=datetime.now(timezone.utc)
meta=json.loads((m.OUT/'metadata.json').read_text(encoding='utf-8-sig'));meta.update(status='CLOSED',end_utc=now.isoformat(),
    substantial_search_count=0,iterative_optimizer_invocations=0,nominal_shape_attempts=0,
    substantial_analysis_batches=9,materially_distinct_attempt_count=0,plateau=False,
    elapsed_minutes=(now-datetime.fromisoformat(meta['start_utc'].replace('Z','+00:00'))).total_seconds()/60,
    stop_reason='Matched sensitivity and bounded compensator comparison answered to available model fidelity',
    completed_candidates=['B05-1','B05-2','B06'],decision='Retain all three; B05-1 provisional lower-risk baseline; next matched thermal/material study',
    resource_note='Elapsed includes reading, coding, reporting and tooling; no quota interruption. Nine analysis batches, no nonlinear optimizer or architecture search.',
    human_intervention='User specified investigation scope and standing push authorization; no optical correction')
m.save('metadata.json',meta);m.save('closure.json',meta)
for p in m.OUT.rglob('*.json'):json.loads(p.read_text(encoding='utf-8-sig'))
files=sorted(p for p in m.OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts)
(m.OUT/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(m.OUT).as_posix()+'\n' for p in files))
print(json.dumps(dict(status='CLOSED',files_hashed=len(files),elapsed_minutes=meta['elapsed_minutes'],validation='PASS')))
