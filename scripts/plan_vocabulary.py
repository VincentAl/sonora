#!/usr/bin/env python3
"""Deterministic vocabulary shortlist; never treats draft/generation as learning."""
import argparse
import datetime as dt
import json
from pathlib import Path


def plan(items, history, today, limit=5, revisit_days=14, revisit_slots=1, diagnostic=None):
    """With a diagnostic, only explicitly learning expressions can be proposed."""
    if diagnostic is not None:
        known_es = set(diagnostic['known'])
        learning_es = set(diagnostic['learning'])
        if known_es & learning_es:
            raise ValueError('diagnostic known/learning overlap')
        if not known_es or not learning_es:
            raise ValueError('diagnostic must include known and learning expressions')
    else:
        known_es, learning_es = set(), set()
    if not 1 <= limit <= 5 or not 0 <= revisit_slots <= limit or revisit_days < 1:
        raise ValueError('invalid planning limits')
    ids = [x['id'] for x in items]
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate vocabulary id')
    known = set(ids)
    published = {}
    latest_event = {}
    stage_order = {'draft': 0, 'generated': 1, 'published': 2}
    for event in history:
        if event['target_id'] not in known:
            raise ValueError('history references unknown target')
        if event['stage'] not in ('draft', 'generated', 'published'):
            raise ValueError('unknown history stage')
        date = dt.date.fromisoformat(event['date'])
        if date > today:
            raise ValueError('future history event')
        if event['stage'] == 'published':
            published.setdefault(event['target_id'], []).append(date)
        event_key = (date, stage_order[event['stage']])
        old = latest_event.get(event['target_id'])
        if old is None or event_key > old[0]:
            latest_event[event['target_id']] = (event_key, event['stage'])
    pending = {id for id, (_, stage) in latest_event.items() if stage != 'published'}
    fresh, revisits = [], []
    for item in items:
        if item['id'] in pending:
            continue
        if diagnostic is None:
            if item['status'] != 'candidate':
                continue
        elif item['es'] not in learning_es or item['es'] in known_es:
            continue
        if item['status'] == 'retired':
            continue
        dates = published.get(item['id'], [])
        priority = item['priority']
        if type(priority) is not int or not 1 <= priority <= 5:
            raise ValueError('priority must be integer 1..5')
        if not dates:
            fresh.append(item)
        elif (today - max(dates)).days >= revisit_days:
            revisits.append((item, max(dates)))
    # A published exposure is not evidence of mastery; this only spaces appearances.
    revisits.sort(key=lambda p: (p[1], -p[0]['priority'], p[0]['id']))
    fresh.sort(key=lambda x: (-x['priority'], x['id']))
    chosen_revisits = [x for x, _ in revisits[:revisit_slots]]
    chosen_fresh = fresh[:limit - len(chosen_revisits)]
    if len(chosen_fresh) < limit - len(chosen_revisits):
        chosen_revisits += [x for x, _ in revisits[len(chosen_revisits):limit - len(chosen_fresh)]]
    return {
        'as_of': today.isoformat(),
        'proposed': [{'id': x['id'], 'es': x['es'], 'fr_sense': x['fr_sense'],
                      'reason': 'revisit' if x['id'] in published else 'new'}
                     for x in chosen_revisits + chosen_fresh],
        'pending_excluded': sorted(pending),
        'note': 'Editorial shortlist only; draft/generated items are reserved, not learned. Human review required.'
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', default='data/vocabulary.json')
    p.add_argument('--as-of', required=True, help='YYYY-MM-DD; explicit for reproducibility')
    p.add_argument('--limit', type=int, default=5)
    p.add_argument('--revisit-days', type=int, default=14)
    p.add_argument('--revisit-slots', type=int, default=1)
    args = p.parse_args()
    source = json.loads(Path(args.data).read_text(encoding='utf-8'))
    if source['version'] != 1:
        p.error('unsupported vocabulary schema version')
    try:
        result = plan(source['targets'], source['history'], dt.date.fromisoformat(args.as_of),
                      args.limit, args.revisit_days, args.revisit_slots,
                      source.get('diagnostic'))
    except (ValueError, KeyError) as exc:
        p.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
