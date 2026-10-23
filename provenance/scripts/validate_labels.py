"""Validate a census output file against its shard id list. Usage: python3 -I provenance/scripts/validate_labels.py shardN.ids outN.jsonl"""
import json, sys
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
T = {'RULE','STEP','DEFINE','FACT','CONSEQ','META'}
M = {'MUST','MUST_NOT','MAY','SHOULD','SHOULD_NOT','NONE'}
B = {'legal','advice','imperative','permission','none'}
CL = {'WHEN','WHILE','ONLY_IF','UNLESS','EXCEPTION_TO','BECAUSE','PURPOSE','IF_VIOLATED','IF_THEN','UNTIL','BEFORE_AFTER','QUANT','DEFAULT'}
DIM = {'location','road_type','lane','time_light','weather_surface','other_road_user','own_vehicle','traffic_control','driver_state','licence','manoeuvre_phase','emergency','other'}
VG = {'J','M','S','R','D','G'}
KEYS = ['id','t','role','m','b','caut','cl','act','ent','dim','fit','need','vg','pass','v']
seen = {}; errs = []
for n, line in enumerate(open(sys.argv[2]), 1):
    line = line.strip()
    if not line: continue
    try: o = json.loads(line)
    except Exception as e: errs.append(f'line {n}: bad JSON {e}'); continue
    miss = [k for k in KEYS if k not in o]
    if miss: errs.append(f'line {n} {o.get("id")}: missing {miss}')
    i = o.get('id')
    if i in seen: errs.append(f'line {n}: duplicate id {i}')
    seen[i] = o
    if o.get('t') not in T: errs.append(f'{i}: bad t {o.get("t")}')
    if o.get('m') not in M: errs.append(f'{i}: bad m {o.get("m")}')
    if o.get('b') not in B: errs.append(f'{i}: bad b {o.get("b")}')
    if o.get('fit') not in ('FULL','PARTIAL','NONE'): errs.append(f'{i}: bad fit')
    for c in o.get('cl') or []:
        if c not in CL: errs.append(f'{i}: bad cl {c}')
    for d in o.get('dim') or []:
        if d not in DIM: errs.append(f'{i}: bad dim {d}')
    for v in o.get('vg') or []:
        if not (isinstance(v, list) and len(v) == 2 and v[0] in VG): errs.append(f'{i}: bad vg {v}')
    if o.get('t') in ('RULE','STEP','DEFINE','CONSEQ') and not o.get('v'): errs.append(f'{i}: missing v rewrite')
missing = [i for i in ids if i not in seen]
extra = [i for i in seen if i not in set(ids)]
print(f'labelled {len(seen)}/{len(ids)}; missing {len(missing)}; extra {len(extra)}; errors {len(errs)}')
for e in errs[:40]: print('  ', e)
if missing: print('  missing ids (first 30):', missing[:30])
if extra: print('  extra ids:', extra[:30])
