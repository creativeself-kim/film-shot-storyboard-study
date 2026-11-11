"""Recompute descriptive results and participant-cluster bootstrap intervals."""
import csv
import hashlib
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent / 'collected_data'
SCENES = ('BAR-P01', 'RET-P01')
QUESTIONS = ('Q1', 'Q2', 'Q3', 'Q4')
SEED = 20260922
RESAMPLES = 20000


def main():
    with (DATA / 'responses.csv').open(encoding='utf-8-sig', newline='') as f:
        responses = list(csv.DictReader(f))
    with (DATA / 'participants.csv').open(encoding='utf-8-sig', newline='') as f:
        participants = list(csv.DictReader(f))
    ids = [p['participant_id'] for p in participants]
    assert len(ids) == len(set(ids)) == 30
    assert len(responses) == 60
    assert {r['participant_id'] for r in responses} == set(ids)
    records = defaultdict(dict)
    for r in responses:
        pid, scene = r['participant_id'], r['scene']
        assert scene in SCENES and scene not in records[pid]
        assert r['condition'] in ('N', 'S') and r['is_synthetic'] == 'False'
        assert all(1 <= int(r[q]) <= 7 for q in QUESTIONS)
        records[pid][scene] = r
    strata = defaultdict(list)
    for p in participants:
        pid = p['participant_id']
        assert set(records[pid]) == set(SCENES)
        assert ''.join(records[pid][s]['condition'] for s in SCENES) == p['condition_pair_BAR_RET']
        first = 'BAR-P01' if p['scene_order'] == 'BAR-first' else 'RET-P01'
        assert records[pid][first]['presentation_order'] == '1'
        assert {r['presentation_order'] for r in records[pid].values()} == {'1', '2'}
        strata[p['condition_pair_BAR_RET'] + '/' + p['scene_order']].append(pid)
    summary = []
    distributions = {}
    for scene in SCENES:
        for condition in ('N', 'S'):
            rows = [r for r in responses if r['scene'] == scene and r['condition'] == condition]
            assert len(rows) == 15
            row = dict(is_synthetic=False, scene=scene, condition=condition, n=len(rows))
            distributions[scene + '/' + condition] = {}
            for q in QUESTIONS:
                values = [int(r[q]) for r in rows]
                row[q + '_mean'] = statistics.mean(values)
                row[q + '_sd'] = statistics.stdev(values)
                counts = Counter(values)
                distributions[scene + '/' + condition][q] = [counts[i] for i in range(1, 8)]
            summary.append(row)

    def differences(sample):
        result = []
        for scene in SCENES:
            sums = {'N': 0, 'S': 0}
            counts = Counter()
            for pid in sample:
                r = records[pid][scene]
                sums[r['condition']] += int(r['Q1'])
                counts[r['condition']] += 1
            result.append(sums['S'] / counts['S'] - sums['N'] / counts['N'])
        return result + [sum(result) / 2]

    rng = random.Random(SEED)
    draws = [[], [], []]
    for _ in range(RESAMPLES):
        sample = [rng.choice(group) for key, group in sorted(strata.items()) for _ in group]
        for values, difference in zip(draws, differences(sample)):
            values.append(difference)
    comparisons = {}
    for label, estimate, values in zip((*SCENES, 'equal_scene_weight'), differences(ids), draws):
        percentiles = statistics.quantiles(values, n=1000, method='inclusive')
        comparisons[label] = {'S_minus_N': estimate, 'ci95': [percentiles[24], percentiles[974]]}
    result = {
        'is_synthetic': False,
        'provenance': 'Author confirmed on 2026-09-22: 30 actual participants with generative-AI content-production experience; prior synthetic/persona annotations were erroneous.',
        'participants': len(ids), 'responses': len(responses),
        'source_sha256': {name: hashlib.sha256((DATA / name).read_bytes()).hexdigest()
                          for name in ('participants.csv', 'responses.csv')},
        'stratum_counts': {key: len(group) for key, group in sorted(strata.items())},
        'summary': summary, 'score_counts_1_to_7': distributions,
        'Q1_comparisons': comparisons,
        'bootstrap': {'resamples': RESAMPLES, 'seed': SEED, 'rng': 'Python random.Random',
                      'method': 'Percentile, linear interpolation; stratified by condition pair and scene order; participant is the resampling unit, retaining both scene responses.'},
        'interpretation': 'Exploratory estimates conditional on these two fixed scene outputs and observed allocation strata; recruitment and randomization procedures are not verified by these files. Q2-Q4 are descriptive secondary outcomes; no multiplicity-adjusted hypothesis tests.'
    }
    (DATA / 'analysis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (DATA / 'summary.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows({k: round(v, 3) if isinstance(v, float) else v for k, v in row.items()} for row in summary)
    print(json.dumps({'strata': result['stratum_counts'], 'Q1': comparisons}, indent=2))


if __name__ == '__main__':
    main()
