# Film-shot-informed storyboard study

논문 재현 자료 및 심사 대응 근거를 정리하는 비공개 작업 저장소입니다. 공개용 배포는 아직 완료되지 않았습니다.

## 참여자 자료
실제 생성형 AI 제작 경험자 30명의 두 장면 응답 60건입니다. 연구자는 2026-11-11 대화에서 이를 재확인했습니다. 기존 SIM/sims 표기와 합성·가상 참여자 설명은 잘못된 메타데이터라는 연구자 설명에 따라 해석합니다. 익명 ID, 조건 배정, 제시 순서, Q1–Q4 응답값은 변경하지 않았습니다. 이 설명은 조사 실시를 별도로 감사했다는 뜻이 아닙니다.

## 재계산
Python 3 표준 라이브러리만 필요합니다.

```sh
python3 evaluation/perceived-clarity-study/analyze_collected_data.py
```

## 제작 기록
`evaluation/novel-continuity-v2/`에 보존된 최종 프롬프트 157개, 구성표와 컷별 상태 지시, 공통 제작 규칙을 수록했습니다. 이는 수정 전후 프롬프트 쌍이 아닙니다. `docs/reviewer-2.md`에서 확인 가능한 범위와 답변 초안을 설명합니다.

## 출처
Google Drive의 연구 데이터 및 그림 / 04 재현 자료 / research-data-and-analysis.zip에 대응하는 기존 로컬 보관본에서 선별했습니다. 이번 작업에서는 Drive 파일 목록과 ZIP 크기를 확인했으며 최신 원격 ZIP과 바이트 단위 동일성은 검증하지 않았습니다. 원본 파일 해시는 `source-manifest.json`에 기록했습니다.

## 제작 보충자료
[보충자료 S](supplementary/README.md) · [본문 보완 및 답변 초안](supplementary/manuscript-and-response.md)
