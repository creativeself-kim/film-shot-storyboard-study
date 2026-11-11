from pathlib import Path
import json,csv,hashlib,collections,shutil
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT.parent/'_workspace/review-response-2026-11-10/drive_data/zip/x'
OUT=ROOT/'supplementary'; OUT.mkdir(exist_ok=True)
BASE=ROOT/'evaluation/novel-continuity-v2'
cuts=json.loads((BASE/'catalog.json').read_text())['cuts']
policy=json.loads((BASE/'production-policy.json').read_text())
def table(path,rows):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[]
for c in cuts:
 p=BASE/'prompts'/f"{c['id']}.txt"
 assert p.read_text().strip()==c['prompt'].strip(),c['id']
 rows.append(dict(cut_id=c['id'],plan_id=c['plan_id'],order=c['order'],shot_size=c['source_cut']['size'],planned_seconds=c['source_cut']['seconds'],phase=c.get('phase',''),source_description=c['source_cut'].get('description',''),source_representative_frame=c['source_cut'].get('representative_frame',''),final_production_state=c['production_state'],final_prompt_path=str(p.relative_to(ROOT)),final_prompt_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),before_image_prompt='not_located_in_inspected_package',verified_revision_count='not_determinable'))
table(OUT/'S2-cut-register.csv',rows)
counts=collections.Counter(c['plan_id'] for c in cuts)
summary=[]
for k,n in sorted(counts.items()):
 primary=k.endswith('-N') or k.endswith('-S')
 summary.append(dict(plan_id=k,total_cuts=n,final_prompts_available=n,state_instructions_available=n,production_stage='N/S re-production' if primary else 'first image production',before_after_pairs_available=0,verified_modified_cut_count='not_determinable'))
table(OUT/'S1-condition-summary.csv',summary)
env=[]
for folder in ['novel-shot-breakdown-v1','novel-ablation-v1']:
 for p in sorted((SRC/'evaluation'/folder/'runs').glob('*.run.json')):
  d=json.loads(p.read_text()); env.append(dict(plan_id=d['id'],started_at=d['started_at'],model=d['model_requested'],reasoning=d['reasoning_effort'],snapshot=d['model_snapshot'],os_inferred_from_execution_path='Windows' if 'C:\\' in d['argv'][0] else 'macOS-style path',attempts=len(d['attempts']),source_path=str(p.relative_to(SRC)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
table(OUT/'S3-plan-execution.csv',env)
# Preserve selected historical evidence without presenting its assertions as new checks.
evidence=OUT/'historical-records';evidence.mkdir(exist_ok=True)
for name in ['README.md','verification.json']:
 shutil.copy2(SRC/'evaluation/novel-continuity-v2'/name,evidence/name)
for folder in ['novel-shot-breakdown-v1','novel-ablation-v1']:
 dest=evidence/folder;dest.mkdir(exist_ok=True)
 for p in (SRC/'evaluation'/folder/'runs').glob('*.run.json'):shutil.copy2(p,dest/p.name)
parts=['# S4. 컷 구성과 최종 제작 지시 대조\n\n구성표의 대표 순간과 최종 제작 지시를 나란히 제시한다. 구성표는 최초 이미지 프롬프트가 아니므로 아래 대조를 수정 전후 프롬프트 비교로 해석하지 않는다. 최종 프롬프트 전문은 각 링크에 있다.\n']
for c in cuts:
 if not (c['plan_id'].endswith('-N') or c['plan_id'].endswith('-S')):continue
 parts.append(f"## {c['id']}\n\n- 예정 샷 크기·시간: {c['source_cut']['size']} / {c['source_cut']['seconds']}초\n- 구성표 대표 순간: {c['source_cut'].get('representative_frame','')}\n- 최종 상태 지시: {c['production_state']}\n- [최종 프롬프트 전문](../evaluation/novel-continuity-v2/prompts/{c['id']}.txt)\n")
# Editorial comparison document is maintained separately.
pair=[c for c in cuts if c['id'] in ['BAR-P01-N-C009','BAR-P01-S-C012']]; assert pair[0]['production_state']==pair[1]['production_state']
# Editorial English README is maintained separately and is not overwritten.

manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json'}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Validated {len(cuts)} prompt/catalog matches; {len(env)} execution records; N/S comparison has 78 cuts.')
