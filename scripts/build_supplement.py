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
(OUT/'S4-NS-production-comparison.md').write_text('\n'.join(parts))
pair=[c for c in cuts if c['id'] in ['BAR-P01-N-C009','BAR-P01-S-C012']]; assert pair[0]['production_state']==pair[1]['production_state']
(OUT/'README.md').write_text('''# 보충자료 S. 제작 기록 및 비교 범위

작성일: 2026-11-11. 보존된 기록을 정리한 사후 자료이며, 당시 작성된 수정 일지를 새로 복원한 것은 아니다.

## S1. 조건별 제작·자료 보존 현황

| 장면 | N | S | S−T | S−D |
|---|---:|---:|---:|---:|
| BAR-P01 | 20 | 26 | 26 | 22 |
| RET-P01 | 17 | 15 | 16 | 15 |

총 157컷의 최종 프롬프트와 상태 지시가 보존되어 있다. 제작 당시 README는 N/S 78장의 재제작과 제거 조건 79장의 최초 제작을 기록한다. 이 수치는 재제작·제작 대상 수이며, 수정 전후 비교로 확정한 수정 컷 수가 아니다. [조건별 표](S1-condition-summary.csv), [전체 컷 목록](S2-cut-register.csv).

검토한 로컬 research-data-and-analysis.zip 추출본의 최초 이미지 제작 폴더에는 start-hashes.json만 있다. 내부 experiment-evidence.zip의 파일 목록에서도 해당 이미지 제작 프롬프트를 찾지 못했다. 따라서 이 패키지에서 확인 가능한 수정 전후 이미지 프롬프트 쌍은 0건이며, 다른 저장소까지 포함한 영구 미보존을 뜻하지 않는다. 최초 프롬프트가 확보되기 전에는 유형별 실제 수정 횟수를 산출할 수 없다.

## S2. 보완 유형과 적용 단위

| 유형 | 보존 기록에서 확인되는 내용 | 집계 해석 |
|---|---|---|
| 공간·행동축 | 인물의 세계 위치, 진행 방향, 카메라가 유지할 축의 한쪽 | 장면별 공통 규칙 |
| 신체 좌우·접촉 | 잡는 손과 잡히는 팔, 공격 손가락과 볼의 해부학적 좌우 | 공통 규칙 및 컷별 상태 |
| 자세·중간 행동 | 엎드림, 올라타기, 잡기 해제, 손 내리기, 보행의 현재 상태 | 컷별 상태 |
| 소품·사건 결과 | 방패 위치, 배낭 소유, 부상, 소멸과 마석 출현 시점 | 공통 규칙 및 컷별 상태 |
| 시간적 혼입 방지 | 앞뒤 대표 순간을 문맥으로 제공하고 현재 순간만 묘사 | 최종 프롬프트 구성 |
| 참조 배경 | 장면별 공통 배경 2장, 기존 소품 혼입 방지 | 당시 제작 기록의 설명 |

이는 보완 내용의 분류이며 독립 코더의 이미지 판독 또는 수정 빈도 분석이 아니다. 최종 지시 157건의 존재를 검증했지만, 각 지시가 최초 프롬프트 대비 새로 추가됐는지는 확정하지 않았다. 구성표의 원래 행동에도 일부 정보가 들어 있다.

[전체 공통 규칙](../evaluation/novel-continuity-v2/production-policy.json), [N/S 78컷 대조](S4-NS-production-comparison.md).

## S3. 동일 사건 비교

BAR-P01 N 9번과 S 12번의 최종 production_state는 문자열 단위로 동일하다. 오른손으로 상대의 왼팔을 잡도록 명시하고, 이후 사건의 마석·소멸 흔적이 나타나지 않도록 제한한다. 두 컷의 전체 프롬프트가 동일하다는 뜻은 아니다. 원래 컷 정보와 앞뒤 문맥은 다를 수 있다. 이 사례는 양쪽에 같은 상태 지시가 제공됐다는 근거이며, 모든 컷에서 보완의 효과가 같았다는 증거는 아니다.

## S4. 실행 환경 및 제작자 조건 인지

N/S 실행 로그는 2026-09-16, S−T·S−D 로그는 2026-09-18을 기록한다. 실행 경로는 각각 macOS 계열과 Windows 경로이다. 모든 요청 모델은 gpt-6-astra, 추론 설정은 medium이며 모델 스냅샷은 공개되지 않았다고 기록한다. [실행 표](S3-plan-execution.csv)와 historical-records의 원본 로그를 함께 제공한다. 원고에 기재된 CLI 0.154.0/0.155.0은 이번에 읽은 run.json 자체에 버전 필드가 없어 독립 확인한 값으로 표시하지 않는다.

당시 제작 README에 기록된 이미지 환경은 Comfy Cloud / OpenAIGPTImageNodeV2, gpt-image-2.5-sunburst, 1536×864, medium, opaque, n=1이다. 같은 기록은 대기열 등록 실패 1건의 동일 입력 재제출과 내용상 실패의 최초 출력 보존을 설명한다. 이 설명은 당시 기록에 근거하며 이번에 서비스 실행 로그나 전체 이미지를 새로 감사한 결과는 아니다.

제작자가 조건을 알고 작업했다는 사실은 연구자의 현행 원고에 명시되어 있다. 공통 제작 규칙을 적용했더라도 제작자 보완의 개별 효과나 조건 간 영향의 동등성을 분리하지 못한다. 해석 대상은 해당 제작 절차를 거친 고정 결과물이다.

## S5. 참여자 자료 출처

연구자는 2026-11-11 실제 참여자 30명의 조사 자료임을 재확인했다. 이전 SIM/sims·합성·가상 참여자 설명은 잘못된 메타데이터라는 설명을 보존했다. 기존 익명 ID, 조건 배정, 제시 순서와 60건의 응답값은 변경하지 않았다. 실제 참여자 조사와 모델을 활용한 제작물 관찰 기록은 별개의 자료이다.

## 자료 사용 범위

현재 저장소는 비공개 작업본이다. 원격 Drive 최신 ZIP과 로컬 보관본의 바이트 단위 동일성, 다른 위치의 최초 프롬프트 보존 여부, 공개 배포 범위는 아직 확인 중이다. 원고에는 공개가 완료되기 전까지 공개 완료로 기재하지 않는다.
''')
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json'}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Validated {len(cuts)} prompt/catalog matches; {len(env)} execution records; N/S comparison has 78 cuts.')
